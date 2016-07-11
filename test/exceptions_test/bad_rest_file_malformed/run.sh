#!/bin/bash

_SCRIPT_DIR=$(dirname ${0})
_TMP="${_SCRIPT_DIR}/.tmp$(date +%s)"

. ${_SCRIPT_DIR}/../../../ci/common.sh

cd ${_SCRIPT_DIR}

restafari -s localhost -p ${TEST_SERVER_PORT} file.rest >> ${_TMP}
cat ${_TMP}

[[ -n "$(grep Trackback $_TMP)" ]] && exit 1
[[ -n "$(grep "malformed" $_TMP)" ]] && exit 0

rm -f ${_TMP}
