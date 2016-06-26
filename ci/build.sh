#!/usr/bin/env bash

. $(dirname ${0})/common.sh

cd ${_RESTAFARI_HOME}

. env.sh

[[ -d build/restafari ]] && rm -rf build/restafari

mkdir -p build/restafari
cp -r src/* build/restafari

$SUCCESS "Checking Python 3 Dependencies" pip install -r ${_RESTAFARI_HOME}/requirements.pip
$WARN "Checking code standards" /bin/bash ${_RESTAFARI_HOME}/test/standards.sh
