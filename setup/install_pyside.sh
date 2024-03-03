#!/bin/bash -e

# Update the package list
sudo apt update

# Install Python3 and pip if they're not installed
sudo apt install -y python3 python3-pip

# Install PySide2 (for Qt5 applications)
pip3 install PySide2

# If you want to install PySide6 (for Qt6 applications), use:
# pip3 install PySide6

echo "PySide installation is complete."
