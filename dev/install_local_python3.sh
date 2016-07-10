#!/bin/bash

# TODO: use virtualenv instead

[[ ${LOCAL_CI} != "1" ]] && echo "
This script creates a local python3 installation, in your home directory. Please run this script has a regular user.

Please make sure that gcc, make, wget and its dependencies are correctly installed. To install, run:

Ubuntu:
   sudo apt-get install build-essential

CentOS/Redhat:
   sudo yum groupinstall 'Development Tools'

Tested on Ubuntu 15.10 and Redhat 6.7.

"

[[ ${USER} = 'root' ]] && echo "Please run it as your user (the user you use to code)!" && exit

cd $(dirname ${0})/..
_RESTAFARI_HOME="$(pwd)"
_HOME_DIR=${HOME}

_ERROR_INST_MSG="Installation aborted. Fix all dependencies to continue!"
echo "Restafari home: ${_RESTAFARI_HOME}"

[[ -z ${PYTHON_VERSION} ]] && PYTHON_VERSION=3.5.1

mkdir -p ${_HOME_DIR}/.tmp 2> /dev/null

if [[ ! -f ${_HOME_DIR}/.apps/python-${PYTHON_VERSION}/bin/python3 ]]; then

  echo " ********************************************************************"
  echo " *** FIRST RUN ON PYTHON ${PYTHON_VERSION}, IT MAY TAKE MORE TIME THAN USUAL ***"
  echo " ********************************************************************"
  echo
  echo "Installing Python ${PYTHON_VERSION} on ${HOME}/.apps/python-${PYTHON_VERSION}"
  cd ${_HOME_DIR}/.tmp
  wget -c "https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz"
  tar xf "Python-${PYTHON_VERSION}.tar.xz"
  cd "Python-${PYTHON_VERSION}"
  PYTHONHOME=${_HOME_DIR}/.apps/python-${PYTHON_VERSION}
  CFLAGS="-w" ./configure --prefix=${PYTHONHOME} --exec-prefix=${PYTHONHOME} > /dev/null; [[ ${?} -gt 0 ]] && echo ${_ERROR_INST_MSG} && exit 1
  make > /dev/null; [[ ${?} -gt 0 ]] && echo ${_ERROR_INST_MSG} && exit 1
  make install > /dev/null; [[ ${?} -gt 0 ]] && echo ${_ERROR_INST_MSG} && exit 1
fi

echo "Python ${PYTHON_VERSION} installed on ${HOME}/.apps/python-${PYTHON_VERSION}"

if [[ ${LOCAL_CI} != "1" ]] && [[ "$(env python3)" != "${HOME}/.apps/python-${PYTHON_VERSION}/bin/python3" ]]; then
  echo "Add the new Python installation in env.sh"
  cd ${_RESTAFARI_HOME}
  echo "" >> ${_RESTAFARI_HOME}/env.sh
  echo "# Added by $(basename ${0}) on $(date)" >> ${_RESTAFARI_HOME}/env.sh
  echo "# Your local Python installation is in ${_HOME_DIR}/.apps/python-${PYTHON_VERSION}/bin directory." >> ${_RESTAFARI_HOME}/env.sh
  echo "export PATH=\"${_HOME_DIR}/.apps/python-${PYTHON_VERSION}/bin:\${ORIG_PATH}\"" >> ${_RESTAFARI_HOME}/env.sh
fi

if [[ ${LOCAL_CI} != "1" ]]; then
  . ${_RESTAFARI_HOME}/env.sh
else
  export PATH="${HOME}/.apps/python-${PYTHON_VERSION}/bin:${PATH}"
fi

echo "python3: $(which python3)"

if [[ ! -f "${HOME}/.apps/python-${PYTHON_VERSION}/bin/pip3" ]]; then
  echo "Installing PIP on ${HOME}/.apps/python-${PYTHON_VERSION}/bin"
  wget -c https://bootstrap.pypa.io/get-pip.py -O ${HOME}/.tmp/get-pip.py
  python3 ${_HOME_DIR}/.tmp/get-pip.py > /dev/null
fi
pip3 install --upgrade pip > /dev/null

[[ ! -f "$(which python3)" ]] && echo "Python3 is not installed properly" && exit 1

echo "PIP3 version: $(pip3 --version)"
