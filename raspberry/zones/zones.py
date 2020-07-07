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
    TOP_RIGHT = 3,
    BOT_LEFT = 4,
    BOT_CENTER = 5,
    BOT_RIGHT = 6,
    BOT_BOT = 7


class Zones:

    api = None
    scanner = None

    # collection_margin = {
    #     Collection.TOP_LEFT: {"left": 50, "top": 50, "right": 50, "bottom": 50},
    #     Collection.TOP_RIGHT: {"left": 50, "top": 50, "right": 50, "bottom": 50},
    #     Collection.BOT_LEFT: {"left": 50, "top": 50, "right": 50, "bottom": 50},
    #     Collection.BOT_RIGHT: {"left": 50, "top": 50, "right": 50, "bottom": 50}
    # }

    # zone_position = {
    #     Zone.TOP_TOP: (0, -125),
    #     Zone.TOP_LEFT: (-100, -25),
    #     Zone.TOP_CENTER: (0, -25),
    #     Zone.TOP_RIGHT: (100, -25),
    #     Zone.BOT_LEFT: (-100, 25),
    #     Zone.BOT_CENTER: (0, 50),
    #     Zone.BOT_RIGHT: (100, 25),
    #     Zone.BOT_BOT: (0, 125)
    # }

    # zone_margin = {
    #     Zone.TOP_TOP: {"left": 75, "top": 0, "right": 75, "bottom": 50},
    #     Zone.TOP_LEFT: {"left": 25, "top": 50, "right": 25, "bottom": 25},
    #     Zone.TOP_CENTER: {"left": 75, "top": 50, "right": 75, "bottom": 25},
    #     Zone.TOP_RIGHT: {"left": 25, "top": 50, "right": 25, "bottom": 25},
    #     Zone.BOT_LEFT: {"left": 25, "top": 25, "right": 25, "bottom": 50},
    #     Zone.BOT_CENTER: {"left": 75, "top": 50, "right": 75, "bottom": 25},
    #     Zone.BOT_RIGHT: {"left": 25, "top": 25, "right": 25, "bottom": 50},
    #     Zone.BOT_BOT: {"left": 75, "top": 50, "right": 75, "bottom": 0}
    # }

    ## Test settings
    collection_margin = {
        Collection.TOP_LEFT: {"left": 25, "top": 25, "right": 25, "bottom": 25},
        Collection.TOP_RIGHT: {"left": 25, "top": 25, "right": 25, "bottom": 25},
        Collection.BOT_LEFT: {"left": 25, "top": 25, "right": 25, "bottom": 25},
        Collection.BOT_RIGHT: {"left": 25, "top": 25, "right": 25, "bottom": 25}
    }

    zone_position = {
        Zone.TOP_TOP: (0, -75),
        Zone.TOP_LEFT: (-50, -12.5),
        Zone.TOP_CENTER: (0, -12.45),
        Zone.TOP_RIGHT: (50, -12.5),
        Zone.BOT_LEFT: (-50, 12.5),
        Zone.BOT_CENTER: (0, 12.5),
        Zone.BOT_RIGHT: (50, 12.5),
        Zone.BOT_BOT: (0, 75)
    }

    zone_margin = {
        Zone.TOP_TOP: {"left": 25, "top": 0, "right": 25, "bottom": 50},
        Zone.TOP_LEFT: {"left": 25, "top": 12.5, "right": 25, "bottom": 12.5},
        Zone.TOP_CENTER: {"left": 25, "top": 12.5, "right": 25, "bottom": 12.5},
        Zone.TOP_RIGHT: {"left": 25, "top": 12.5, "right": 25, "bottom": 12.5},
        Zone.BOT_LEFT: {"left": 25, "top": 12.5, "right": 25, "bottom": 12.5},
        Zone.BOT_CENTER: {"left": 25, "top": 12.5, "right": 25, "bottom": 12.5},
        Zone.BOT_RIGHT: {"left": 25, "top": 12.5, "right": 25, "bottom": 12.5},
        Zone.BOT_BOT: {"left": 25, "top": 50, "right": 25, "bottom": 0}
    }


    def __init__(self, api, scanner) -> None:
        self.api = api
        self.scanner = scanner


    def at_collection(self) -> bool:
        collection = self.selected_collection()
        margin = self.collection_margin[collection]

        beacon_pos = self.selected_collection_position()
        cart_pos = self.scanner.current_cart_pos()

        beacon_margin_left      = float(beacon_pos[0] - margin["left"])
        beacon_margin_top       = float(beacon_pos[1] + margin["top"])
        beacon_margin_right     = float(beacon_pos[0] + margin["right"])
        beacon_margin_bottom    = float(beacon_pos[1] - margin["bottom"])

        in_horizontal   = beacon_margin_left < cart_pos[0] < beacon_margin_right
        in_vertical     = beacon_margin_top > cart_pos[1] > beacon_margin_bottom

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

    
    def in_zone(self) -> bool:
        zone = self.selected_zone()
        margin = self.zone_margin[zone]

        zone_pos = self.zone_position[zone]
        cart_pos = self.scanner.current_cart_pos()

        zone_margin_left      = float(zone_pos[0] - margin["left"])
        zone_margin_top       = float(zone_pos[1] + margin["top"])
        zone_margin_right     = float(zone_pos[0] + margin["right"])
        zone_margin_bottom    = float(zone_pos[1] - margin["bottom"])

        in_horizontal   = zone_margin_left < cart_pos[0] < zone_margin_right
        in_vertical     = zone_margin_top > cart_pos[1] > zone_margin_bottom

        return in_horizontal and in_vertical

    def selected_zone(self) -> Zone:
        zone_api_points = {
            1: Zone.TOP_TOP,
            3: Zone.TOP_LEFT,
            4: Zone.TOP_CENTER,
            5: Zone.TOP_RIGHT,
            6: Zone.BOT_LEFT,
            7: Zone.BOT_CENTER,
            8: Zone.BOT_RIGHT,
            10: Zone.BOT_BOT
        }

        zone_id = self.api.webserver.zone

        return zone_api_points.get(zone_id, None)

    def selected_collection_position(self) -> Tuple[int, int]:
        id = self.selected_collection().value

        return self.scanner.beacons[id].position

    def selected_zone_position(self) -> Tuple[int, int]:
        id = self.selected_zone()

        return self.zone_position[id]

    def selected_collection_rotation(self, x: float, y: float) -> float:
        (col_x, col_y) = self.selected_collection_position()

        delta_x = col_x - x
        delta_y = col_y - x

        rotation_radian = math.atan2(delta_x, delta_y)

        return math.degrees(rotation_radian)

    def selected_zone_rotation(self, x: float, y: float) -> float:
        (zone_x, zone_y) = self.selected_zone_position()

        delta_x = zone_x - x
        delta_y = zone_y - x

        rotation_radian = math.atan2(delta_x, delta_y)

        return math.degrees(rotation_radian)
