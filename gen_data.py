import numpy as np
import pandas as pd

def make_time_series(n=2000, seed=42, anomaly_strength=1.0, folding=True):
    assert n > 200, "n greater than 200"
    rng = np.random.default_rng(seed)
    t = np.arange(n)

    # -------------------------
    # BASE STRUCTURE (strong periodic geometry)
    # -------------------------
    trend = 0.001 * t

    yearly = 2.2 * np.sin(2 * np.pi * t / 80)
    weekly = 0.7 * np.sin(2 * np.pi * t / 12)

    # adds curvature → helps create stable H1 baseline
    slow_modulation = 0.4 * np.sin(2 * np.pi * t / 90)

    noise = rng.normal(0, 0.2, size=n)

    x = trend + yearly + weekly + slow_modulation + noise

    # correlated channels → needed for meaningful embedding geometry
    x2 = np.roll(x, 7) + rng.normal(0, 0.1, n)
    x3 = np.roll(x, 13) - 0.5 * x + rng.normal(0, 0.1, n)

    # -------------------------
    # STRONG ANOMALY TYPES (GEOMETRY BREAKING)
    # -------------------------

    # 1. PERIODICITY BREAK (DESTROYS H1 STRUCTURE)
    for _ in range(3):
        start = rng.integers(n // 4, 3 * n // 4)
        max_len = min(150, n - start)
        length = rng.integers(80, max_len)
    
        phase_shift = np.linspace(0, np.pi * anomaly_strength, length)
    
        x[start:start+length] += 2.5 * np.sin(phase_shift)
        x2[start:start+length] -= 1.5 * np.cos(phase_shift)
        x3[start:start+length] += rng.normal(0, 0.4, length)

    # 2. GEOMETRIC FOLDING (CREATES FAKE LOOPS / DISTORTS H1)
    if folding:
        for _ in range(4):
            start = rng.integers(0, n - 50)
            max_len = min(120, n - start)
            length = rng.integers(50, max_len)
        
            end = start + length
        
            segment = x[start:end].copy()
        
            # nonlinear warp → changes topology
            warped = np.tanh(segment * anomaly_strength) * 3
        
            noise = rng.normal(0, 0.2, size=length)
        
            x[start:end] = warped
            x2[start:end] = np.roll(warped, 3)
            x3[start:end] = -warped + noise

    # 3. REGIME SHIFT (BIG GLOBAL STRUCTURE CHANGE)
    shift_start = rng.integers(n // 3, 2 * n // 3)
    shift_length = 200

    x[shift_start:shift_start+shift_length] += 4 * anomaly_strength
    x2[shift_start:shift_start+shift_length] -= 3 * anomaly_strength
    x3[shift_start:shift_start+shift_length] += 2 * anomaly_strength

    # 4. LOCAL PERIOD DESTRUCTION (BREAKS LOOP CONSISTENCY)
    for _ in range(2):
        start = rng.integers(0, n - 200)
        length = 200

        x[start:start+length] += rng.normal(
            0,
            1.5 * anomaly_strength,
            size=length
        )

    df = pd.DataFrame({
        "t": t,
        "x": x,
        "x2": x2,
        "x3": x3
    })

    return df
