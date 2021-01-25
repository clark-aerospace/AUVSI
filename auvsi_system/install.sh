#!/bin/bash

echo "Installing dependencies"
pip install mavsdk
pip install --upgrade matplotlib
apt install libgeos-dev -y
pip install https://github.com/matplotlib/basemap/archive/master.zip
apt-get install proj-bin -y