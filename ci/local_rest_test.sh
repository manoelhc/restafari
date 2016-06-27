#!/usr/bin/env bash

. $(dirname ${0})/common.sh

bash ${_RESTAFARI_HOME}/ci/show_python_info.sh; [[ $? -gt 0 ]] && exit 1

cd ${_RESTAFARI_HOME}

chmod +x ${TEST_SERVER}

${TEST_SERVER} ${TEST_SERVER_PORT} &> /dev/null &
sleep 5

for f in $(find test/rests/pass -name '*.rest'); do
  # $FAILURE "Running $f" coverage run
  $(which restafari.py) --port ${TEST_SERVER_PORT} --hostname localhost $f
done

kill $(ps aux | grep -F ${TEST_SERVER} | grep -v grep | awk '{print $2}') 2> /dev/null
exit 0
