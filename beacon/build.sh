#!/bin/bash

port=/dev/ttyUSB0
#port=/dev/cu.usbmodem1412301

set -e

arduino-cli compile --fqbn esp32:esp32:WeMosBat --build-path $(pwd)/out
arduino-cli upload -p $port --fqbn esp32:esp32:WeMosBat
screen -L $port 115200

# To quit the screen session use Ctrl + A + K
