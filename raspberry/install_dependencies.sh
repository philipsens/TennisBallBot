#!/bin/bash

# Install libedgetpu library

echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get -y install libedgetpu1-std

# Install npm

sudo apt-get -y install npm

# Beacons

sudo apt-get -y install libbluetooth-dev
sudo apt-get -y install python3-dev libbluetooth-dev libcap2-bin
sudo setcap 'cap_net_raw,cap_net_admin+eip' $(readlink -f $(which python3))

# Get packages required for OpenCV

sudo apt-get -y install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt-get -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get -y install libxvidcore-dev libx264-dev
sudo apt-get -y install qt4-dev-tools libatlas-base-dev

# Install python requirements

pip3 install -r requirements.txt

# Get packages required for TensorFlow

version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')

if [ $version == "3.7" ]; then
pip3 install https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp37-cp37m-linux_armv7l.whl
fi

if [ $version == "3.5" ]; then
pip3 install https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp35-cp35m-linux_armv7l.whl
fi
