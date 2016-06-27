#!/usr/bin/env bash

. $(dirname ${0})/common.sh

cd ${_RESTAFARI_HOME}

cd build

python3 setup.py install

echo "Python3 binary: $(which python3)"
echo "PATH: ${PATH}"
echo "Restafari binary: $(which restafari.py)"
echo "PYTHONHOME=${PYTHONHOME}"
echo "PYTHONPATH=${PYTHONPATH}"
