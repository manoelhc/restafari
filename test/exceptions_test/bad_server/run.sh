#!/bin/bash

_SCRIPT_DIR=$(dirname ${0})
_TMP="${_SCRIPT_DIR}/.tmp$(date +%s)"

. ${_SCRIPT_DIR}/../../../ci/common.sh

cd ${_SCRIPT_DIR}

echo "-- TESTING FAKE HOSTNAME --"
restafari -s this.is.a.fake.hostname.to.nowhere -p ${TEST_SERVER_PORT} file.rest > ${_TMP}
cat ${_TMP}
[[ -n "$(grep Trackback $_TMP)" ]] && exit 1

echo "-- TESTING FAKE PORT NUMBER --"
restafari -s localhost -p 118 file.rest > ${_TMP}
cat ${_TMP}
[[ -n "$(grep Trackback $_TMP)" ]] && exit 1



rm -f ${_TMP}
