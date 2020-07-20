#!/bin/bash

cd ./src

docker build -t server -f server/Dockerfile .
docker build -t client -f client/Dockerfile .

cd ../
docker-compose up 
