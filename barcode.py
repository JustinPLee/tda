from matplotlib import pyplot as plt
import numpy as np

def plot_betti_barcode(diagram, homology_dim):
    diagram = np.asarray(diagram)

    mask = diagram[:, 2] == homology_dim
    birth = diagram[mask, 0]
    death = diagram[mask, 1]

    if len(birth) == 0:
        print(f"No H{homology_dim} features found.")
        return

    persistence = death - birth

    # sort by persistence (largest first)
    order = np.argsort(-persistence)
    birth = birth[order]
    death = death[order]

    fig, ax = plt.subplots(figsize=(8, 4))

    y = 0
    for b, d in zip(birth, death):
        if d <= b:
            continue
        ax.hlines(y, b, d, linewidth=2)
        y += 1

    ax.set_xlabel("Filtration scale (ε)")
    ax.set_ylabel("Feature index")
    ax.set_title(f"Betti Barcode (H{homology_dim})")

    plt.tight_layout()
    plt.show()