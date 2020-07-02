#include "SerialManager.h"

namespace ZumoAPI {

    SerialManager::SerialManager(SerialCallback callback) {
        Serial.begin(115200);
        this->callback = callback;
    }

    void SerialManager::poll() {

        const char carriage_return = '\r';
        const char new_line = '\n';
        const uint16_t two_seconds = 2000;
        char read;
        unsigned long current_millis = millis();


        while (Serial.available() > 0) {
            read = Serial.read();

            if (read != new_line && read != carriage_return) {
                this->buffer[this->buffer_index % 256] = read;
                this->buffer_index++;

            } else {
                if (this->buffer_index == 0)
                    continue;

                this->buffer[this->buffer_index % 256] = '\0';
                this->buffer_index = 0;

                this->last_serial_response = millis();
                this->callback(this->buffer);
            }
        }

        if (current_millis - this->last_serial_response < two_seconds) {
            this->callback('stop;')
        }
    }
    
};