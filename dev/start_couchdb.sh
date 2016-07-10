#!/bin/bash
cd $(dirname ${0})

./stop_couchdb.sh
sudo docker rm -f restafari-test
sudo docker run -d --name restafari-test -p 5984:5984 couchdb
sudo docker ps
