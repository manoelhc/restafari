#!/bin/bash

for f in $(find ../src -name '*.py'); do
  pep8 --first $f
done