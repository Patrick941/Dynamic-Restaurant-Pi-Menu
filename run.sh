#!/bin/bash
rm -rf /home/restuarant1/piMenu
cd /home/restaurant1

git clone https://github.com/Patrick941/Dynamic-Restaurant-Pi-Menu piMenu
cd piMenu

menuVenv/bin/python piMenu/menu.py

