#!/bin/bash

echo "
This is the regular dependency installer for UNIX environments which has Python 3.x pre-installed.
If you don't have it install on your system, please install it before going on! If the package system
you're using does not install python3, please try to run install_full_dev.sh.

"

if [[ ${USER} != root ]]; then
  echo "Please run this script as a root user!"
  exit
fi

if [[ ! -f "$(which pip3)" ]]; then
  echo "You need to install Python 3.x first!"
  exit
fi

pip3 install --upgrade pip
pip3 install -r ../requirements.pip
