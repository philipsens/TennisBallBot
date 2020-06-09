import time
from beacontools import BeaconScanner, IBeaconFilter

def callback(bt_addr, rssi, packet, additional_info):
#    print("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))
    distance = 10 ** ((packet.tx_power - rssi) / (10 * 1))
    print("distance: %f" % distance)

# scan for all iBeacon advertisements from beacons with the specified uuid 
scanner = BeaconScanner(callback, 
    device_filter=IBeaconFilter(uuid="00000000-0000-0000-0000-000000000000")
)
scanner.start()
#time.sleep(5)
#scanner.stop()
