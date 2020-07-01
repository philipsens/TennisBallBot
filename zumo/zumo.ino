#include <ZumoShield.h>

#include "SerialManager.h"
#include "ZumoMotor.h"

ZumoAPI::ZumoMotor motor;
ZumoAPI::SerialManager serial = NULL;

void processToken(const char* identifier, const char* value) {

    // The "move" command moves both the tracks in the same direction to go backwards or forwards
    if (strcmp(identifier, "move") == 0) {
        int16_t speed = atoi(value);

        motor.leftTrack(speed);
        motor.rightTrack(speed);
        motor.update();

        Serial.print("move=");
        Serial.println(speed);

    } else
    // The "left" command moves the left track backwards and the right track forwards so the cart turns to the left
    if (strcmp(identifier, "left") == 0) {
        int16_t speed = atoi(value);

        motor.rightTrack(speed);
        motor.update();

        Serial.print("left=");
        Serial.println(speed);

    } else
    // The "ball-left" command moves the right track forwards so the cart turns to the left
    if (strcmp(identifier, "right") == 0) {
        int16_t speed = atoi(value);

        motor.leftTrack(speed);
        motor.update();

        Serial.print("right=");
        Serial.println(speed);

    } else
    if (strcmp(identifier, "center-left") == 0) {
        int16_t speed = atoi(value);

        motor.leftTrack(-speed);
        motor.rightTrack(speed);
        motor.update();

        Serial.print("center-left=");
        Serial.println(speed);

    } else
    if (strcmp(identifier, "center-right") == 0) {
        int16_t speed = atoi(value);

        motor.leftTrack(-speed);
        motor.rightTrack(speed);
        motor.update();

        Serial.print("center-right=");
        Serial.println(speed);

    } else
    // Goose goes "honks"
    if (strcmp(identifier, "honk") == 0) {
        ZumoBuzzer buzzer;
        buzzer.playNote(3 + 5 * 12, 250, 15);

        Serial.println("honk");
    } else
    if (strcmp(identifier, "stop") == 0) {
        reset();
        Serial.println("stopped");

    } else {
        Serial.println("Not a valid action, resetting");
        reset(); // Incase of failed action
        return;
    }

}

void reset() {
    motor.leftTrack(0);
    motor.rightTrack(0);
    motor.update();
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
