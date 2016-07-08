#!/usr/bin/env bash

. $(dirname ${0})/common.sh

cd ${_RESTAFARI_HOME}

# pip3 uninstall -y restafari

[[ -d build/restafari ]] && rm -rf build

mkdir -p build/restafari
cp -r src/* build/restafari

cp_version=$(curl "https://pypi.python.org/pypi?name=restafari&:action=display_pkginfo" 2>/dev/null| egrep '^Version:' | awk '{print $2}')
cg_version=$(git tag | tail -n1 | awk '{print $1}')

cpv_major=$(echo ${cp_version} | cut -d. -f1)
cpv_minor=$(echo ${cp_version} | cut -d. -f2)
cpv_rel=$(echo ${cp_version} | cut -d. -f3)

cpg_major=$(echo ${cg_version} | cut -d. -f1)
cpg_minor=$(echo ${cg_version} | cut -d. -f2)
cpg_rel=$(echo ${cg_version} | cut -d. -f3)

build_version=

if [[ ${cpv_major} -eq ${cpg_major} ]]; then
  if [[ ${cpv_minor} -eq ${cpg_minor} ]]; then
    build_version="${cpv_major}.${cpv_minor}.$(( ${cpv_rel} + 1 ))"
  else
    build_version="${cpv_major}.${cpg_minor}.$(( ${cpg_rel} + 1 ))"
  fi
else
  build_version="${cpg_major}.${cpg_minor}.$(( ${cpg_rel} + 1 ))"
fi

cat setup.py | sed "s,{{RESTAFARI_VERSION}},${build_version},g" > build/setup.py
cp setup.cfg build/
cp LICENSE build/LICENSE.txt
cp README.md build/

$WARN "Checking code standards" /bin/bash ${_RESTAFARI_HOME}/test/standards.sh