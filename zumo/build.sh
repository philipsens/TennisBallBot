#!/bin/bash

port=/dev/ttyACM0

set -e

arduino-cli compile --fqbn arduino:avr:uno --build-path $(pwd)/out
arduino-cli upload -p $port --fqbn arduino:avr:uno
screen $port 115200

# To quit the screen sessions use CTRL + A -> K
