#!/bin/bash

echo "Installing dependencies"
pip install mavsdk django django-jsonify
pip install --upgrade matplotlib
pip install https://github.com/matplotlib/basemap/archive/master.zip
apt-get install proj-bin libgeos-dev -y
