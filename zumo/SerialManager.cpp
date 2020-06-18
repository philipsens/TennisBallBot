#include "SerialManager.h"

namespace ZumoAPI {

    SerialManager::SerialManager(SerialCallback callback) {
        Serial.begin(115200);
        this->callback = callback;
    }

    void SerialManager::poll() {

        static char carriage_return = '\r';
        static char new_line = '\n';
        char read;

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

                this->callback(this->buffer);
            }
        }
    }
    
};