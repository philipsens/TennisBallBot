#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEBeacon.h>
#include "esp_sleep.h"
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"
#include "resources.h"

BLEAdvertising *ble_advertising;

void create_beacon() {
    BLEBeacon beacon = BLEBeacon();
    beacon.setManufacturerId(0x4C00); // Fake Apple manufacturer id
    beacon.setProximityUUID(BLEUUID(resource_uuid));
    beacon.setMajor(resource_major);
    beacon.setMinor(resource_minor);
    beacon.setSignalPower(0xC1);

    BLEAdvertisementData advertisement_data = BLEAdvertisementData();
    BLEAdvertisementData scan_response_data = BLEAdvertisementData();

    advertisement_data.setFlags(0x04);

    std::string service_data = "";
  
    service_data += (char) 0x1A; // Len
    service_data += (char) 0xFF; // Type
    service_data += beacon.getData();

    advertisement_data.addData(service_data);

    ble_advertising->setAdvertisementData(advertisement_data);
    ble_advertising->setScanResponseData(scan_response_data);
}

void setup() {
    // Disable the Brownout check (Need to find a better powersupply)
    WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);
    Serial.begin(115200);
    pinMode(LED_BUILTIN, OUTPUT);

    BLEDevice::init("");
    ble_advertising = BLEDevice::getAdvertising();
    
    create_beacon();
}

void loop() {
    
    Serial.printf("starting advertising\r\n");
    ble_advertising->start();
    delay(100);
    ble_advertising->stop();
    Serial.printf("stopping advertising\r\n");

    delay(100);
}
