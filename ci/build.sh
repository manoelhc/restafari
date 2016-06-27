#!/usr/bin/env bash

. $(dirname ${0})/common.sh

cd ${_RESTAFARI_HOME}

pip3 uninstall -y restafari

[[ -d build/restafari ]] && rm -rf build/restafari

mkdir -p build/restafari
cp -r src/* build/restafari

git tag | tail -n1 > build/VERSION

cat build/VERSION

cp setup.py build/
cp setup.cfg build/
cp LICENSE build/LICENSE.txt
cp README.md build/

$SUCCESS "Checking Python 3 Dependencies" pip install -r ${_RESTAFARI_HOME}/requirements.pip
$WARN "Checking code standards" /bin/bash ${_RESTAFARI_HOME}/test/standards.sh

chmod +x build/restafari/restafari.py
