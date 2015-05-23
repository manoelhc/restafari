#!/bin/bash
PWD=$(dirname $0)
cd $PWD
TEST_SERVER="server/restserver.py"
SUCCESS="/bin/bash ${PWD}/scripts/runtest.sh SUCCESS"
WARN="/bin/bash ${PWD}/scripts/runtest.sh WARNING"
FAILURE="/bin/bash ${PWD}/scripts/runtest.sh FAILURE"

$SUCCESS "Checking Python 3 Dependencies" sudo pip3 install -r ../requirements.pip
$WARN "Checking code standards" /bin/bash ./standards.sh


chmod +x $TEST_SERVER
server/restserver.py &> /dev/null &
cd ../src
chmod +x restafari.py
sleep 5


for f in $(ls ../test/rests/pass/*.rest); do
  $SUCCESS "Running $f" ./restafari.py  --port 8080 --hostname localhost $f
done

kill $(ps aux | grep -F $TEST_SERVER | grep -v grep | awk '{print $2}')
echo "Test DONE"