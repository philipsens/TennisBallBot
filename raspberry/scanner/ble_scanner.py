import time
from typing import Tuple
from beacontools import BeaconScanner, IBeaconFilter
import scanner

class BLEBeacon:
    position = None
    results = None
    index = 0
    max_len = 0

    def calculate_distance(rssi: int, tx_power: int) -> float:
        return (10 ** ((tx_power - rssi) / (10 * 2))) * 10

    def __init__(self, max_len: int, position: Tuple[int, int]) -> None:
        # Preallocate the array for faster inserts
        self.results = max_len * [0]
        self.max_len = max_len
        self.position = position

    def push(self, value: float) -> None:
        key = (self.index + 1) % self.max_len
        self.index = key

        self.results[self.index] = value

    def avg(self) -> float:
        sum_results = sum(self.results)
        return sum_results / self.max_len


class BLEScanner:
    scanner = None
    beacons = None

    def __init__(self, uuid: str) -> None:
        self.scanner = BeaconScanner(self.callback, 
            device_filter=IBeaconFilter(uuid=uuid)
        )

        beacon_size = 10

        self.beacons = [
            BLEBeacon(beacon_size, (-5,  5)),
            BLEBeacon(beacon_size, ( 5,  5)),
            BLEBeacon(beacon_size, (-5, -5)),
            BLEBeacon(beacon_size, ( 5, -5))
        ]

    def callback(self, bt_addr, rssi, packet, additional_info) -> None:
        if (additional_info["major"] > len(self.beacons)):
            print("Out of bound beacon", file=sys.stderr)
            return

        major = int(additional_info["major"])

        beacon = self.beacons[major]
        distance = BLEBeacon.calculate_distance(rssi, packet.tx_power)
        beacon.push(distance)

        print("[BLEScanner] beacon: %d, distance: %f, avg: %f" % (major, distance, beacon.avg()))
    
    def cart_position(self) -> Tuple[float, float]:
        top_horizontal  = (self.beacons[0].avg() + -self.beacons[1].avg()) / 10
        bot_horizontal  = (self.beacons[2].avg() + -self.beacons[3].avg()) / 10

        left_vertical   = (self.beacons[0].avg() + -self.beacons[2].avg()) / 10
        right_vertical  = (self.beacons[1].avg() + -self.beacons[3].avg()) / 10

        horizontal  = (top_horizontal + bot_horizontal) / 2
        vertical    = (left_vertical + right_vertical) / 2

        return (horizontal, vertical)

    def start(self) -> None:
        self.scanner.start()

    def stop(self) -> None:
        self.scanner.stop()
