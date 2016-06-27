#!/usr/bin/env bash

. $(dirname ${0})/common.sh

cd ${_RESTAFARI_HOME}

cd build

python3 setup.py install

bash ${_RESTAFARI_HOME}/ci/show_python_info.sh; [[ $? -gt 0 ]] && exit 1