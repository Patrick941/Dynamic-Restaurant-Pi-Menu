#!/bin/bash
alias python=python3

python -m venv menuVenu
source menuVenu/bin/activate
pip install pillow
sudo apt update
sudo apt install python3-tk
