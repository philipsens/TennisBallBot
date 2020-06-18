#include "ZumoMotor.h"

namespace ZumoAPI {

    void ZumoMotor::leftTrack(int16_t speed) {
        this->leftTrackSpeed = speed;
    }

    void ZumoMotor::rightTrack(int16_t speed) {
        this->rightTrackSpeed = speed;
    }

    void ZumoMotor::move(int16_t speed) {
        this->leftTrack(speed);
        this->rightTrack(speed);
    }

    void ZumoMotor::update() {
        this->motors.setSpeeds(
            this->leftTrackSpeed,
            this->rightTrackSpeed
        );
    }
}