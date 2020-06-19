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
        return (10 ** ((tx_power - rssi) / (10 * 1.75))) * 10


    def calculate_accuracy(rssi: int, tx_power: int) -> float:
        if (rssi == 0):
            return -1
        
        ratio = rssi / tx_power

        if ratio < 1:
            return ratio ** 10
        else:
            return 0.89976 * (ratio ** 7.7095) + 0.111

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

        self.beacons = [ # Every beacon is 1 meter apart from each other 
            BLEBeacon(beacon_size, (-50,  50)),
            BLEBeacon(beacon_size, ( 50,  50)),
            BLEBeacon(beacon_size, (-50, -50)),
            BLEBeacon(beacon_size, ( 50, -50))
        ]

    def callback(self, bt_addr, rssi, packet, additional_info) -> None:
        if (additional_info["major"] > len(self.beacons)):
            print("Out of bound beacon", file=sys.stderr)
            return

        major = int(additional_info["major"])

        beacon = self.beacons[major]
        distance = BLEBeacon.calculate_distance(rssi, packet.tx_power)
        accuracy = BLEBeacon.calculate_accuracy(rssi, packet.tx_power)
        beacon.push(distance)

        print("[BLEScanner] beacon: %d, distance: %f, accuracy: %f, avg: %f" % (major, distance, accuracy, beacon.avg()))
    
    def cart_position(self) -> Tuple[float, float]:

        # Calculate the distance between the points
        distance_horizontal = abs(self.beacons[0].position[0] - self.beacons[1].position[0])
        distance_vertical   = abs(self.beacons[0].position[1] - self.beacons[2].position[1])

        center_horizontal = distance_horizontal / 2
        center_vertical   = distance_vertical / 2

        min_top_horizontal = self.beacons[0].position[0] + self.beacons[0].avg()
        max_top_horizontal = self.beacons[1].position[0] + self.beacons[1].avg()

        min_bot_horizontal = self.beacons[2].position[0] + self.beacons[2].avg()
        max_bot_horizontal = self.beacons[3].position[0] + self.beacons[3].avg()

        space_top_horizontal = distance_horizontal - (self.beacons[0].avg() + self.beacons[1].avg())
        space_bot_horizontal = distance_horizontal - (self.beacons[2].avg() + self.beacons[3].avg())

        min_left_vertical = self.beacons[2].position[1] + self.beacons[2].avg()
        max_left_vertical = self.beacons[0].position[1] + self.beacons[0].avg()

        min_right_vertical = self.beacons[3].position[1] + self.beacons[3].avg()
        max_right_vertical = self.beacons[1].position[1] + self.beacons[1].avg()

        space_left_vertical  = distance_vertical - (self.beacons[0].avg() + self.beacons[2].avg())
        space_right_vertical = distance_vertical - (self.beacons[1].avg() + self.beacons[3].avg())

        # Very inaccurate but can be used to estimate the accurate beacon
        avg_horizontal  = (min_top_horizontal + space_top_horizontal / 2) + (min_bot_horizontal + space_bot_horizontal / 2) / 2
        avg_vertical    = (min_left_vertical + space_left_vertical / 2) + (min_right_vertical + space_right_vertical / 2)
        
        print(avg_horizontal, avg_vertical)

        vertical, vertical_radius = (0, 0)

        # if true, take the right side beacons, else the left
        if avg_horizontal > center_horizontal:
            vertical_radius = space_right_vertical / 2
            vertical = min_right_vertical + vertical_radius
        else: 
            vertical_radius = space_left_vertical / 2
            vertical = min_left_vertical + vertical_radius

        horizontal, horizontal_radius = (0, 0)

        if avg_vertical > center_vertical:
            horizontal_radius = space_top_horizontal / 2
            horizontal = min_top_horizontal + horizontal_radius
        else:
            horizontal_radius = space_bot_horizontal / 2
            horizontal = min_bot_horizontal + horizontal_radius
        
        return (horizontal, vertical)

    def start(self) -> None:
        self.scanner.start()

    def stop(self) -> None:
        self.scanner.stop()
