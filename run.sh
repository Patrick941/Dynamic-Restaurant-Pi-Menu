#!/bin/bash
cd /home/restaurant1/piMenu

git reset --hard HEAD
git pull origin master

source setup.sh
menuVenv/bin/python piMenu/menu.py

