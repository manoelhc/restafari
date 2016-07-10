#!/usr/bin/env bash

. $(dirname ${0})/common.sh
[[ -f ${_RESTAFARI_HOME}/env.sh ]] && . ${_RESTAFARI_HOME}/env.sh

cd  ${_RESTAFARI_HOME}


pip3 install -e .
python3 setup.py install

[[ -z $(which restafari 2>/dev/null) ]] && echo "Restafari is not installed properly" && exit 1
restafari --version

[[ ${?} -gt 0 ]] && echo "Restafari is not installed properly" && exit 1

exit 0
