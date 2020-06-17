#include "serial_manager.h"

void callback(char* buffer) {
    Serial.println(buffer);
}

ZumoAPI::SerialManager serial = NULL;

void setup() {
    serial = ZumoAPI::SerialManager(callback);
}

void loop() {
    serial.poll();
}
