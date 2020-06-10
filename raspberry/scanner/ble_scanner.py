import time
from beacontools import BeaconScanner, IBeaconFilter

class BLEScanner:
    scanner = None

    def callback(self, bt_addr, rssi, packet, additional_info):
        distance = 10 ** ((packet.tx_power - rssi) / 10)
        print("distance: %f" % distance)

    def start(self, uuid: str):
        scanner = BeaconScanner(self.callback, 
            device_filter=IBeaconFilter(uuid=uuid)
        )

        scanner.start()

    def stop(self):
        if (scanner == None): return

        scanner.stop()
