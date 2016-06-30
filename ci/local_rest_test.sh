#!/usr/bin/env bash

. $(dirname ${0})/common.sh

cd ${_RESTAFARI_HOME}

chmod +x ${TEST_SERVER}

${TEST_SERVER} ${TEST_SERVER_PORT} &> /dev/null &
sleep 5

for f in $(find test/rests/pass -name '*.rest'); do
  $FAILURE "Running $f" coverage run $(which restafari) --port ${TEST_SERVER_PORT} --hostname localhost $f
done

kill $(ps aux | grep -F ${TEST_SERVER} | grep -v grep | awk '{print $2}') 2> /dev/null
exit 0
