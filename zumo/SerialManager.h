#include <HardwareSerial.h>

namespace ZumoAPI {
    typedef void (*SerialCallback)(char buffer[]);

    class SerialManager {
    public:
        SerialManager(SerialCallback);
        void poll();
    private:
        uint8_t buffer_index;
        char buffer[256];
        SerialCallback callback;
        unsigned long last_serial_response = millis();
    };

}