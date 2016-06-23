#!/bin/bash

cd $(dirname ${0})
cd ..
. ${_SCRIPT_DIR}/env.sh


for f in $(find src -name '*.py'); do
  pep8 --first $f
done
