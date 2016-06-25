#!/usr/bin/env bash

_SCRIPT_PATH=$(dirname ${0})

cd ${_SCRIPT_PATH}
. env.sh
mkdir -p build/restafari
cp -r src/* build/restafari

TEST_SERVER="${_SCRIPT_PATH}/test/server/restserver.py"
TEST_SERVER_PORT=18080
SUCCESS="/bin/bash ${_SCRIPT_PATH}/test/scripts/runtest.sh SUCCESS"
WARN="/bin/bash ${_SCRIPT_PATH}/test/scripts/runtest.sh WARNING"
FAILURE="/bin/bash ${_SCRIPT_PATH}/test/scripts/runtest.sh FAILURE"

$SUCCESS "Checking Python 3 Dependencies" pip3 install -r ${_SCRIPT_PATH}/requirements.pip
$WARN "Checking code standards" /bin/bash ${_SCRIPT_PATH}/test/standards.sh

${_SCRIPT_PATH}/test/standards.sh

chmod +x ${TEST_SERVER}

${_SCRIPT_PATH}/test/server/restserver.py ${TEST_SERVER_PORT} &> /dev/null &
sleep 5

cd ${_SCRIPT_PATH}/build/restafari
chmod +x restafari.py

cd ${_SCRIPT_PATH}/../..

for f in $(find test/rests/pass -name '*.rest'); do
  $WARN "Running $f" ${_SCRIPT_PATH}/build/restafari/restafari.py --port ${TEST_SERVER_PORT} --hostname localhost $f
done

kill $(ps aux | grep -F ${TEST_SERVER} | grep -v grep | awk '{print $2}') 2> /dev/null
echo "Test DONE"
