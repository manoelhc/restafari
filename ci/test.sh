#!/usr/bin/env bash

. $(dirname ${0})/common.sh
[[ -f ${_RESTAFARI_HOME}/env.sh ]] && . ${_RESTAFARI_HOME}/env.sh

cd ${_RESTAFARI_HOME}

# Test role processing

for f in $(ls ${_RESTAFARI_HOME}/test/rests/pass/*.rest); do
  $SUCCESS "Running $f" ${RESTAFARI_CMD} --port ${TEST_SERVER_PORT} --hostname localhost $f
  [[ ${?} -gt 0 ]] && echo "Test failed!" && exit 1
done
echo "Test DONE"
