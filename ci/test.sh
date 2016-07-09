#!/usr/bin/env bash

. $(dirname ${0})/common.sh
cd ${_RESTAFARI_HOME}

# Test role processing

chmod +x $TEST_SERVER
${TEST_SERVER} ${TEST_SERVER_PORT} &> /dev/null &
sleep 5

for f in $(ls ${_RESTAFARI_HOME}/test/rests/pass/*.rest); do
  $SUCCESS "Running $f" ${RESTAFARI_CMD}  --port ${TEST_SERVER_PORT} --hostname localhost $f
done

kill $(ps aux | grep -F $TEST_SERVER | grep -v grep | awk '{print $2}')
echo "Test DONE"