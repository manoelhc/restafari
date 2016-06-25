#!/bin/bash

echo "
This script creates a local python3 installation, in your home directory. Please run this script has a regular user.

Please make sure that gcc, make, wget and its dependencies are correctly installed. To install, run:

Ubuntu:
   sudo apt-get install build-essential

CentOS/Redhat:
   sudo yum groupinstall 'Development Tools'

Tested on Ubuntu 15.10 and Redhat 6.7.

"

[[ ${USER} = 'root' ]] && echo "Please run it as your user (the user you use to code)!" && exit

cd $(dirname ${0})
_SCRIPT_DIR="$(pwd)"
_HOME_DIR=${HOME}

PYTHON_VERSION=3.5.1

if [[ ! -f ${_HOME_DIR}/.apps/python-${PYTHON_VERSION}/bin/python3 ]] || [[ "$(env python3 2> /dev/null;echo $?)" -gt 0 ]]; then
  mkdir ${_HOME_DIR}/.tmp
  cd ${_HOME_DIR}/.tmp
  wget -c "https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz" #|| echo "Error on download Python!" && exit 1
  tar xf "Python-${PYTHON_VERSION}.tar.xz" #|| echo "Error on untar the python.tar.xz file!" && exit 1
  cd "Python-${PYTHON_VERSION}"
  ./configure --prefix=${_HOME_DIR}/.apps/python-${PYTHON_VERSION} #|| echo "Error on configuring python for compiling" && exit 1
  make  #|| echo "Error on runnning make command!" && exit 1
  make install  #|| echo "Error on running make install command" && exit 1
  cd ${_SCRIPT_DIR}/..

  echo "" >> ${_SCRIPT_DIR}/../env.sh
  echo "# Added by $(basename ${0}) on $(date)" >> ${_SCRIPT_DIR}/../env.sh
  echo "# Your local Python installation is in ${_HOME_DIR}/.apps/python-${PYTHON_VERSION}/bin directory." >> ${_SCRIPT_DIR}/../env.sh
  echo "export PATH=\"${_HOME_DIR}/.apps/python-${PYTHON_VERSION}/bin:\${ORIG_PATH}\"" >> ${_SCRIPT_DIR}/../env.sh
fi

. ${_SCRIPT_DIR}/../env.sh

pip3 install --upgrade pip  #|| echo "Error on installing python3 dependency!" && exit 1
pip3 install -r ${_SCRIPT_DIR}/../requirements.pip
