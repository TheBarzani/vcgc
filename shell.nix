# let
#   pkgs = import <nixpkgs> {};
# in pkgs.mkShell {
#   packages = [
#     (pkgs.python310.withPackages (python-pkgs: [
#       python-pkgs.pandas
#       python-pkgs.requests
#       python-pkgs.ipykernel
#     ]))
#   ];
# }

with import <nixpkgs> { };

let
  pythonPackages = python310Packages; # Change to Python 3.10
in pkgs.mkShell rec {
  name = "impurePythonEnv";
  venvDir = "./.venv";
  buildInputs = [

    pkgs.stdenv.cc.cc.lib

    git-crypt

    pythonPackages.python
    pythonPackages.ipykernel
    pythonPackages.pyzmq    # Adding pyzmq explicitly
    pythonPackages.venvShellHook
    pythonPackages.pip
    pythonPackages.numpy
    pythonPackages.pandas
    pythonPackages.requests

    # sometimes you might need something additional like the following - you will get some useful error if it is looking for a binary in the environment.
    taglib
    openssl
    git
    libxml2
    libxslt
    libzip
    zlib

  ];

  # Run this command, only after creating the virtual environment
  postVenvCreation = ''
    unset SOURCE_DATE_EPOCH
    
    python -m ipykernel install --user --name=myenv4 --display-name="myenv4"
    pip install -r requirements.txt
  '';

  # Now we can execute any commands within the virtual environment.
  # This is optional and can be left out to run pip manually.
  postShellHook = ''
    # allow pip to install wheels
    unset SOURCE_DATE_EPOCH
  '';
}