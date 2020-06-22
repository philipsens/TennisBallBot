#include <ZumoShield.h>

#include "SerialManager.h"
#include "ZumoMotor.h"

ZumoAPI::ZumoMotor motor;
ZumoAPI::SerialManager serial = NULL;

void processToken(const char* identifier, const char* value) {

    if (strcmp(identifier, "left") == 0) {
        int16_t speed = atoi(value);

        motor.leftTrack(speed);

        Serial.print("left=");
        Serial.println(speed);
    } else
    if (strcmp(identifier, "right") == 0) {
        int16_t speed = atoi(value);

        motor.rightTrack(speed);

        Serial.print("right=");
        Serial.println(speed);
    } else
    if (strcmp(identifier, "honk") == 0) {
        ZumoBuzzer buzzer;
        buzzer.playNote(3 + 5 * 12, 250, 15);

        Serial.println("honk");
    }

}

void processLine(char* line) {
    const char* delimiter = "=";

    const char* identifier  = strtok_r(line, delimiter, &line);
    const char* value       = strtok_r(line, delimiter, &line);

    processToken(identifier, value);
}

void callback(char* buffer) {
    const char* delimiter = ";";
    char* token;

    while ((token = strtok_r(buffer, delimiter, &buffer))) {
        processLine(token);
    }
}

void setup() {
    serial = ZumoAPI::SerialManager(callback);
}

void loop() {
    serial.poll();
    motor.update();
}
