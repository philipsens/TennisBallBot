import sys
import math
from typing import Tuple
from .beacon import BLEBeacon
from beacontools import BeaconScanner, IBeaconFilter


class BLEScanner:
    scanner = None
    beacons = None

    current_beacon_location = None
    last_beacon_location = None

    def __init__(self, uuid: str) -> None:
        self.scanner = BeaconScanner(self.callback,
                                     device_filter=IBeaconFilter(uuid=uuid)
                                     )

        beacon_size = 50

        self.beacons = [  # Every beacon is 1 meter apart from each other
            BLEBeacon(beacon_size, (-50, 50)),
            BLEBeacon(beacon_size, (50, 50)),
            BLEBeacon(beacon_size, (-50, -50)),
            BLEBeacon(beacon_size, (50, -50))
        ]

    def callback(self, bt_addr, rssi, packet, additional_info) -> None:
        if additional_info["major"] > len(self.beacons):
            print("Out of bound beacon", file=sys.stderr)
            return

        major = int(additional_info["major"])

        beacon = self.beacons[major]
        distance = BLEBeacon.calculate_distance(rssi, packet.tx_power)
        beacon.push(distance)

    def cart_position(self) -> Tuple[float, float]:
        distance_horizontal = abs(self.beacons[0].position[0] - self.beacons[1].position[0])
        distance_vertical = abs(self.beacons[0].position[1] - self.beacons[2].position[1])

        min_top_horizontal = self.beacons[0].position[0] + self.beacons[0].avg()
        min_bot_horizontal = self.beacons[2].position[0] + self.beacons[2].avg()

        space_top_horizontal = distance_horizontal - (self.beacons[0].avg() + self.beacons[1].avg())
        space_bot_horizontal = distance_horizontal - (self.beacons[2].avg() + self.beacons[3].avg())

        min_left_vertical = self.beacons[2].position[1] + self.beacons[2].avg()
        min_right_vertical = self.beacons[3].position[1] + self.beacons[3].avg()

        space_left_vertical = distance_vertical - (self.beacons[0].avg() + self.beacons[2].avg())
        space_right_vertical = distance_vertical - (self.beacons[1].avg() + self.beacons[3].avg())

        # Find the closest average distance of the 2 beacons
        # and use those are more "accurate" beacons
        top_avg_distance = self.beacons[0].avg() + self.beacons[1].avg()
        bot_avg_distance = self.beacons[2].avg() + self.beacons[3].avg()

        left_avg_distance = self.beacons[0].avg() + self.beacons[2].avg()
        right_avg_distance = self.beacons[1].avg() + self.beacons[3].avg()

        # Pick side determined by the biggest average
        if right_avg_distance < left_avg_distance:
            vertical_radius = space_right_vertical / 2
            vertical = min_right_vertical + vertical_radius
        else:
            vertical_radius = space_left_vertical / 2
            vertical = min_left_vertical + vertical_radius

        if top_avg_distance < bot_avg_distance:
            horizontal_radius = space_top_horizontal / 2
            horizontal = min_top_horizontal + horizontal_radius
        else:
            horizontal_radius = space_bot_horizontal / 2
            horizontal = min_bot_horizontal + horizontal_radius

        return horizontal, vertical

    def update_location(self) -> None:
        self.last_beacon_location = self.current_beacon_location
        self.current_beacon_location = self.cart_position()

    def cart_rotation(self) -> float:

        delta_x = self.current_beacon_location[0] - self.last_beacon_location[0]
        delta_y = self.current_beacon_location[1] - self.last_beacon_location[1]

        rotation_radian = math.atan2(delta_x, delta_y)

        return math.degrees(rotation_radian)

    def start(self) -> None:
        self.scanner.start()

    def stop(self) -> None:
        self.scanner.stop()
