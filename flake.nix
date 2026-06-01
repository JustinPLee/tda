{
  description = "python + uv";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = import nixpkgs {inherit system;};
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python311
            uv
            stdenv.cc.cc
            zlib
          ];
          shellHook = ''
            export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [
              pkgs.stdenv.cc.cc
              pkgs.zlib
            ]}:$LD_LIBRARY_PATH
            # Create a virtual environment if it doesn't exist
            if [ ! -d ".venv" ]; then
              uv venv .venv
            fi
            # Activate the virtual environment
            source .venv/bin/activate
            # Alias pip to uv for faster package installation
            alias pip="uv pip"
            # auto start jupyter lab
            uv run jupyter lab
          '';
        };
      }
    );
}
