import math
from enum import Enum
from typing import Tuple

class Collection(Enum):
    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOT_LEFT = 2
    BOT_RIGHT = 3


class Zone(Enum):
    TOP_TOP = 0,
    TOP_LEFT = 1,
    TOP_CENTER = 2,
    TOP_RIGHT = 3


class Zones:

    api = None
    scanner = None

    collection_margin = {
        Collection.TOP_LEFT: {"left": 25, "top": 25, "right": 25, "bottom": 25},
        Collection.TOP_RIGHT: {"left": 25, "top": 25, "right": 25, "bottom": 25},
        Collection.BOT_LEFT: {"left": 25, "top": 25, "right": 25, "bottom": 25},
        Collection.BOT_RIGHT: {"left": 25, "top": 25, "right": 25, "bottom": 25}
    }


    def __init__(self, api, scanner) -> None:
        self.api = api
        self.scanner = scanner


    def at_collection(self) -> bool:
        collection = self.selected_collection()
        margin = self.collection_margin[collection]

        beacon_pos = self.selected_collection_position()
        cart_pos = self.scanner.cart_position()

        beacon_margin_left      = float(beacon_pos[0] - margin["left"])
        beacon_margin_top       = float(beacon_pos[1] + margin["top"])
        beacon_margin_right     = float(beacon_pos[0] + margin["right"])
        beacon_margin_bottom    = float(beacon_pos[1] - margin["bottom"])

        in_horizontal   = beacon_margin_left < cart_pos[0] < beacon_margin_right
        in_vertical     = beacon_margin_top > cart_pos[1] > beacon_margin_right

        return in_horizontal and in_vertical

    def collection_from_beacon_id(self, id: int) -> Collection:
        collection_api_points = {
            0: Collection.TOP_LEFT,
            1: Collection.TOP_RIGHT,
            2: Collection.BOT_LEFT,
            3: Collection.BOT_RIGHT
        }

        return collection_api_points.get(id, None) 

    def selected_collection(self) -> Collection:
        collection_api_points = {
            0: Collection.TOP_LEFT,
            2: Collection.TOP_RIGHT,
            9: Collection.BOT_LEFT,
            11: Collection.BOT_RIGHT
        }

        collection_id = self.api.webserver.collection

        return collection_api_points.get(collection_id, None)

    def selected_collection_position(self) -> Tuple[int, int]:
        id = self.selected_collection().value

        return self.scanner.beacons[id].position

    def selected_collection_rotation(self, x: float, y: float) -> float:
        (col_x, col_y) = self.selected_collection_position()

        delta_x = x + col_x
        delta_y = y + col_y

        rotation_radian = math.atan2(delta_x, delta_y)

        return math.degrees(rotation_radian)

    def in_zone(self) -> bool:
        return False

    def selected_zone(self) -> int:
        print(self.api.webserver.collection)
        pass
