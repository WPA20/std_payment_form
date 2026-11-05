#!/bin/bash

read -p "Enter Git Commit Message:__" COMMIT_MSG

echo "Checking Git Status"
git status

echo "Git Add"
git add .

git commit -m "$COMMIT_MSG"

echo "Using Push Command"
git push

echo "Building and Starting Docker Compose..."
docker compose -f std-compose.yml up -d --build

echo "Checking Docker Containers..."
docker compose -f std-compose.yml ps

echo "Successfully Completed! Enjoy!"



