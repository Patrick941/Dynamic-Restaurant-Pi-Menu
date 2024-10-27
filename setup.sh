#!/bin/bash

$(which python3) -m venv menuVenv
source menuVenv/bin/activate
pip install pillow
sudo apt update
sudo apt install python3-tk
