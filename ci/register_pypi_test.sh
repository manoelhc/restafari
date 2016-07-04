#!/usr/bin/env bash

. $(dirname ${0})/common.sh

cat ${_RESTAFARI_HOME}/pypirc.tpl | sed "s,%username%,${PYPI_CRED1},g" | sed "s,%password%,${PYPI_CRED2},g" > ${HOME}/.pypirc
cd ${_RESTAFARI_HOME}/build
pwd

python3 setup.py sdist bdist --formats=gztar,zip upload -r pypitest
