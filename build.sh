#!/usr/bin/env bash

_SCRIPT_PATH=$(dirname ${0})

cd ${_SCRIPT_PATH}
. env.sh
mkdir -p build/restafari
cp -r src/* build/restafari

TEST_SERVER="${_SCRIPT_PATH}/test/server/restserver.py"
SUCCESS="/bin/bash ${_SCRIPT_PATH}/test/scripts/runtest.sh SUCCESS"
WARN="/bin/bash ${_SCRIPT_PATH}/test/scripts/runtest.sh WARNING"
FAILURE="/bin/bash ${_SCRIPT_PATH}/test/scripts/runtest.sh FAILURE"

$SUCCESS "Checking Python 3 Dependencies" sudo pip3 install -r ../requirements.pip
$WARN "Checking code standards" /bin/bash ./standards.sh

chmod +x ${TEST_SERVER}
${_SCRIPT_PATH}/server/restserver.py &> /dev/null &
cd ${_SCRIPT_PATH}/build/restafari
chmod +x restafari.py

for f in $(ls ${_SCRIPT_PATH}/test/rests/pass/*.rest); do
  $SUCCESS "Running $f" ./restafari.py  --port 8080 --hostname localhost $f
done

kill $(ps aux | grep -F ${TEST_SERVER} | grep -v grep | awk '{print $2}') 2> /dev/null
echo "Test DONE"
