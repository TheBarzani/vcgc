with import <nixpkgs> { };

let
  pythonPackages = python310Packages; # Change to Python 3.10
in pkgs.mkShell rec {
  name = "impurePythonEnv";
  venvDir = "./.venv";
  buildInputs = [
    # Keep all your existing dependencies
    pkgs.stdenv.cc.cc.lib
    git-crypt
    pythonPackages.python
    pythonPackages.ipykernel
    pythonPackages.pyzmq
    pythonPackages.venvShellHook
    pythonPackages.pip
    pythonPackages.numpy
    pythonPackages.pandas
    pythonPackages.requests
    pythonPackages.networkx
    pythonPackages.matplotlib
    # Add build dependencies
    pythonPackages.setuptools
    pythonPackages.wheel
    pythonPackages.scikit-build
    pkgs.cmake
    pkgs.ninja
    # C++ specific tools needed for compilation
    pkgs.gcc
    pkgs.gnumake
    # System libraries
    taglib
    openssl
    git
    libxml2
    libxslt
    libzip
    zlib
  ];
  
  # Fix for C++ library loading issues
  shellHook = ''
    # Make libraries available to the Python environment
    export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH
    
    # Make sure both your local package and the venv packages are accessible
    export PYTHONPATH="$PWD:$PWD/${venvDir}/lib/python3.10/site-packages:$PYTHONPATH"

  '';

  # Run this command, only after creating the virtual environment
  postVenvCreation = ''
    unset SOURCE_DATE_EPOCH
    
    python -m ipykernel install --user --name=myenv4 --display-name="myenv4"
    
    # Install base packages first
    pip install --upgrade pip setuptools wheel
    pip install cmake ninja scikit-build
    
    # Install other packages directly
    pip install networkx matplotlib numpy
  '';

  postShellHook = ''
    # allow pip to install wheels
    unset SOURCE_DATE_EPOCH
    
    # Print environment info for debugging
    echo "Python path: $(which python)"
    echo "PYTHONPATH: $PYTHONPATH"
    echo "LD_LIBRARY_PATH: $LD_LIBRARY_PATH"
  '';
}