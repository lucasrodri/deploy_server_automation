#!/bin/bash

# Store git config, for saving credentials
#git config credential.helper store

# Change directory to app folder
cd /home/user/myapp

# Deployment execution
echo "Shutting down containers"
docker-compose down

echo "Pulling new code from repository"
export HOME=/home/user
git config --global --add safe.directory /home/user/myapp
git pull

echo "Building new containers"
docker-compose up -d --build
