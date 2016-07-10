#!/bin/bash
cd $(dirname ${0})

for i in $(sudo docker ps | grep -v 'CONTAINER' | grep 'restafari-test' | awk '{print $1}'); do
  sudo docker stop $i
done
