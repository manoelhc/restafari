#!/bin/bash
cd $(dirname ${0})
_SCRIPT_DIR=$(pwd)
_TMP="${_SCRIPT_DIR}/.tmp$(date +%s)"

. ${_SCRIPT_DIR}/../../../ci/common.sh

cd ${_SCRIPT_DIR}

restafari -s localhost -p ${TEST_SERVER_PORT} file.rest >> ${_TMP}
cat ${_TMP}

[[ -n "$(grep Trackback $_TMP)" ]]   && rm -f ${_TMP} && exit 1
[[ -n "$(grep "malformed" $_TMP)" ]] && rm -f ${_TMP} && exit 0
exit 1
