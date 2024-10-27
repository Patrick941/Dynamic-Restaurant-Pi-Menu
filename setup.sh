#!/bin/bash

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "This script must be sourced. Run 'source ./setup.sh' instead of './setup.sh'"
    exit 1
fi

$(which python3) -m venv menuVenv
source menuVenv/bin/activate
pip install pillow
sudo apt update
sudo apt install python3-tk
