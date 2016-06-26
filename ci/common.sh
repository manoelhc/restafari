#!/usr/bin/env bash

cd $(dirname ${0})/../
_RESTAFARI_HOME=$(pwd)

. ${_RESTAFARI_HOME}/env.sh

TEST_SERVER="${_RESTAFARI_HOME}/test/server/restserver.py"
TEST_SERVER_PORT=18080
SUCCESS="/bin/bash ${_RESTAFARI_HOME}/test/scripts/runtest.sh SUCCESS"
WARN="/bin/bash ${_RESTAFARI_HOME}/test/scripts/runtest.sh WARNING"
FAILURE="/bin/bash ${_RESTAFARI_HOME}/test/scripts/runtest.sh FAILURE"

get_python_path() {
  echo ${HOME}/.apps/python-${1}/bin
}