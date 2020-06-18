#include <ZumoShield.h>

namespace ZumoAPI
{
    class ZumoMotor {
    public:
        void leftTrack(int16_t speed);
        void rightTrack(int16_t speed);

        void move(int16_t speed);
        void update();
    private:
        int16_t leftTrackSpeed = 0;
        int16_t rightTrackSpeed = 0;
        ZumoMotors motors;
    };
}