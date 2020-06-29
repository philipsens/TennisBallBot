#include <ZumoShield.h>

#include "SerialManager.h"
#include "ZumoMotor.h"

ZumoAPI::ZumoMotor motor;
ZumoAPI::SerialManager serial = NULL;

void processToken(const char* identifier, const char* value, const char* time) {
    int32_t wait_time = atoi(time);

    // The "move" command moves both the tracks in the same direction to go backwards or forwards
    if (strcmp(identifier, "move") == 0) {
        int16_t speed = atoi(value);

        motor.leftTrack(speed);
        motor.rightTrack(speed);
        motor.update();

        Serial.print("move=");
        Serial.print(speed);
        Serial.print("=");
        Serial.println(wait_time);

    } else
    // The "left" command moves the left track backwards and the right track forwards so the cart turns to the left
    if (strcmp(identifier, "left") == 0) {
        int16_t speed = atoi(value);

        motor.leftTrack(-speed);
        motor.rightTrack(speed);
        motor.update();

        Serial.print("left=");
        Serial.print(speed);
        Serial.print("=");
        Serial.println(wait_time);
    } else
    // The "right" command moves the left track forwards and the right track backwards so the cart turns to the right
    if (strcmp(identifier, "right") == 0) {
        int16_t speed = atoi(value);

        motor.leftTrack(speed);
        motor.rightTrack(-speed);
        motor.update();

        Serial.print("right=");
        Serial.print(speed);
        Serial.print("=");
        Serial.println(wait_time);
    } else
    // Goose goes "honks"
    if (strcmp(identifier, "honk") == 0) {
        ZumoBuzzer buzzer;
        buzzer.playNote(3 + 5 * 12, 250, 15);

        Serial.println("honk");
    } else {
        Serial.println("Not a valid action");
        return;
    }

    Serial.println("Starting action");

    // Keep executing the command for n amount of time.
    delay(wait_time);

    Serial.println("Stopping action");

    // Set the motors to idle after executing the action.
    reset();
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
    const char* time        = strtok_r(line, delimiter, &line);

    processToken(identifier, value, time);
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
