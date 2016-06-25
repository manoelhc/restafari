#!/bin/bash

_STD_SCRIPT_PATH=$(dirname ${0})
cd ${_STD_SCRIPT_PATH}
_STD_SCRIPT_PATH=$(pwd)

. ${_STD_SCRIPT_PATH}/../env.sh
EXIT=0

for f in $(find ${_STD_SCRIPT_PATH}/../build/restafari -name '*.py'); do
  pep8 --ignore=E111 -- --first $f
  [[ ${?} -gt 0 ]] && EXIT=1
done

exit ${EXIT}
