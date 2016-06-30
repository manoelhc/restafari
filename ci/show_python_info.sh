#!/usr/bin/env bash

echo "Python3 binary: $(which python3)"
echo "PATH: ${PATH}"
echo "Restafari binary: $(which restafari)"
echo "PYTHONHOME=${PYTHONHOME}"
echo "PYTHONPATH=${PYTHONPATH}"
which restafari > /dev/null
if [[ $? -gt 0 ]]; then
  echo "Restafari is not installed correctly"
  exit 1
fi