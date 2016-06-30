#!/usr/bin/env bash

. $(dirname ${0})/common.sh

cd ${_RESTAFARI_HOME}

cd build

pip install -e .

python3 setup.py install

status=$?

bash ${_RESTAFARI_HOME}/ci/show_python_info.sh

exit ${status}