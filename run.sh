#!/bin/bash
cd /home/restaurant1/piMenu

git reset --hard HEAD
output=$(git pull origin master)

if [[ $output == *"Already up to date."* ]]; then
  echo "No changes pulled from GitHub."
else
  source setup.sh
fi

# menuVenv/bin/python menu.py

sleep 1
xdotool search --name "Restaurant Menu" windowactivate
