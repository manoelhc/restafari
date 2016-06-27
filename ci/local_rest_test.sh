#!/usr/bin/env bash

. $(dirname ${0})/common.sh

cd ${_RESTAFARI_HOME}

chmod +x ${TEST_SERVER}

${TEST_SERVER} ${TEST_SERVER_PORT} &> /dev/null &
sleep 5

cd ${_RESTAFARI_HOME}

for f in $(find test/rests/pass -name '*.rest'); do
  $WARN "Running $f" coverage run restafari --port ${TEST_SERVER_PORT} --hostname localhost $f
done

kill $(ps aux | grep -F ${TEST_SERVER} | grep -v grep | awk '{print $2}') 2> /dev/null
exit 0
