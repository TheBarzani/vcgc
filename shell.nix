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
    exec zsh
    # Make libraries available to the Python environment
    export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH
    
    # Make sure both your local package and the venv packages are accessible
    export PYTHONPATH="$PWD:$PWD/${venvDir}/lib/python3.10/site-packages:$PYTHONPATH"
    
    # Ensure __init__.py exists
    mkdir -p $PWD/vcgc
    touch $PWD/vcgc/__init__.py
  '';

  # Run this command, only after creating the virtual environment
  postVenvCreation = ''
    unset SOURCE_DATE_EPOCH
    
    python -m ipykernel install --user --name=myenv4 --display-name="myenv4"
    pip install -r requirements.txt
    pip install networkx matplotlib numpy  # Added numpy explicitly
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

# with import <nixpkgs> { };

# let
#   pythonPackages = python310Packages; # Change to Python 3.10
# in pkgs.mkShell rec {
#   name = "impurePythonEnv";
#   venvDir = "./.venv";
#   buildInputs = [

#     pkgs.stdenv.cc.cc.lib

#     git-crypt

#     pythonPackages.python
#     pythonPackages.ipykernel
#     pythonPackages.pyzmq    # Adding pyzmq explicitly
#     pythonPackages.venvShellHook
#     pythonPackages.pip
#     pythonPackages.numpy
#     pythonPackages.pandas
#     pythonPackages.requests

#     # sometimes you might need something additional like the following - you will get some useful error if it is looking for a binary in the environment.
#     taglib
#     openssl
#     git
#     libxml2
#     libxslt
#     libzip
#     zlib

#   ];

#   # Run this command, only after creating the virtual environment
#   postVenvCreation = ''
#     unset SOURCE_DATE_EPOCH
    
#     python -m ipykernel install --user --name=myenv4 --display-name="myenv4"
#     pip install -r requirements.txt
#   '';

#   # Now we can execute any commands within the virtual environment.
#   # This is optional and can be left out to run pip manually.
#   postShellHook = ''
#     # allow pip to install wheels
#     unset SOURCE_DATE_EPOCH
#   '';
# }