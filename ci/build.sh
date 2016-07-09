#!/usr/bin/env bash

. $(dirname ${0})/common.sh

cd ${_RESTAFARI_HOME}

rm -rf dist
rm -rf build

# Syntax Checker
EXIT=0
for f in $(find ./restafari -name '*.py'); do
  pep8 --ignore=E111 --first $f
  [[ ${?} -gt 0 ]] && EXIT=1
done

[[ ${EXIT} -gt 0 ]] && exit 1


# Remove old restafari
[[ -n "$(which restafari 2>/dev/null)" ]] && restafari --version | awk '{print $2}' >/tmp/restafari_last_installed_version && pip3 uninstall -y restafari 2>/dev/null

build_version=
cg_version=$(git tag | tail -n1 | awk '{print $1}')

# TravisCI-Only
if [[ -n DEBIAN_FRONTEND ]]; then
    cp_version=$(curl "https://pypi.python.org/pypi?name=restafari&:action=display_pkginfo" 2>/dev/null| egrep '^Version:' | awk '{print $2}')

    cpv_major=$(echo ${cp_version} | cut -d. -f1)
    cpv_minor=$(echo ${cp_version} | cut -d. -f2)
    cpv_rel=$(echo ${cp_version} | cut -d. -f3)

    cpg_major=$(echo ${cg_version} | cut -d. -f1)
    cpg_minor=$(echo ${cg_version} | cut -d. -f2)
    cpg_rel=$(echo ${cg_version} | cut -d. -f3)

    # Version Checker

    if [[ ${cpv_major} -eq ${cpg_major} ]]; then
      if [[ ${cpv_minor} -eq ${cpg_minor} ]]; then
        build_version="${cpv_major}.${cpv_minor}.$(( ${cpv_rel} + 1 ))"
      else
        build_version="${cpv_major}.${cpg_minor}.$(( ${cpg_rel} + 1 ))"
      fi
    else
      build_version="${cpg_major}.${cpg_minor}.$(( ${cpg_rel} + 1 ))"
    fi
else
  if [[ -f /tmp/restafari_last_installed_version ]]; then
     build_version=$(cat /tmp/restafari_last_installed_version)
  else
     build_version=${cg_version}
  fi
fi

# Create setup.py with the correct version

cat setup.py.tpl | sed "s,{{RESTAFARI_VERSION}},${build_version},g" > setup.py
exit $?