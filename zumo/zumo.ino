#include "SerialManager.h"
#include "ZumoMotor.h"

ZumoAPI::ZumoMotor motor;
ZumoAPI::SerialManager serial = NULL;

void processToken(const char* identifier, const char* value) {

    if (strcmp(identifier, "left") == 0) {
        int16_t speed = atoi(value);

        motor.leftTrack(speed);
    } else
    if (strcmp(identifier, "right") == 0) {
        int16_t speed = atoi(value);

        motor.rightTrack(speed);
    }

}

void processLine(char* line) {
    const char* delimiter = "=";

    const char* identifier = strtok(line, delimiter);
    const char* value = strtok(NULL, delimiter);

    processToken(identifier, value);
}

void callback(char* buffer) {
    const char* delimiter = ";";
    char* token;

    token = strtok(buffer, delimiter);


    while (token != NULL) {
        processLine(token);

        token = strtok(NULL, delimiter);
    }

}

void setup() {
    serial = ZumoAPI::SerialManager(callback);
}

void loop() {
    serial.poll();
    motor.update();
}
