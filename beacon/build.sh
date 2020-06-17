#!/bin/bash

set -e

uuid="00000000-0000-0000-0000-000000000000"
major=${1:-0}
minor=${2:-0}

resource_header="/* This is an auto-generated header file from the build script */\r\n"

resource_header+="const std::string resource_uuid = \"$uuid\";\r\n"
resource_header+="const uint8_t resource_major = $major;\r\n"
resource_header+="const uint8_t resource_minor = $minor;\r\n"

printf "$resource_header" > "resources.h"

echo "Flashing beacon with major: $major and minor: $minor"

port=/dev/ttyUSB0
#port=/dev/cu.usbmodem1412301

arduino-cli compile --fqbn esp32:esp32:WeMosBat --build-path $(pwd)/out
arduino-cli upload -p $port --fqbn esp32:esp32:WeMosBat
screen -L $port 115200

# To quit the screen session use Ctrl + A + K
