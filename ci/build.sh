#!/usr/bin/env bash

. $(dirname ${0})/common.sh

cd ${_RESTAFARI_HOME}

# pip3 uninstall -y restafari

[[ -d build/restafari ]] && rm -rf build

mkdir -p build/restafari
cp -r src/* build/restafari

git tag | tail -n1 > build/VERSION

cat build/VERSION

cp setup.py build/
cp setup.cfg build/
cp LICENSE build/LICENSE.txt
cp README.md build/

$WARN "Checking code standards" /bin/bash ${_RESTAFARI_HOME}/test/standards.sh
