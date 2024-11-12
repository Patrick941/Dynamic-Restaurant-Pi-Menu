#!/bin/bash
cd /home/restaurant1/piMenu

git pull origin master

menuVenv/bin/python piMenu/menu.py

