{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    # C++ compiler and build tools
    gcc
    gnumake
    cmake

    # Python and core packages
    python3
    python3Packages.pip
  ];
  
  shellHook = ''
    echo "Quantum computing development environment ready!"
    echo "Use 'jupyter notebook' to start Jupyter."
    
    # Create local venv if it doesn't exist
    if [ ! -d .venv ]; then
      python -m venv .venv
    fi
    source .venv/bin/activate
  '';
}