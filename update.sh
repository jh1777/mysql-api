#!/bin/bash

echo "<<< Stop old docker container >>>" 
docker stop mysql-api-container

echo "<<< Remove old docker container >>>" 
docker rm mysql-api-container

echo "<<< Pull latest chnages from Git Repo >>>" 
git pull

echo "<<< Build new docker image >>>" 
docker build -t mysql-api .

echo "<<< Run the new docker image as mysql-api-container >>>" 
docker run --name mysql-api-container -d -p 4568:8080 mysql-api

echo "<<< Remove all unused images >>>" 
docker image prune -a --force