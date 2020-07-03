import math
import time
from .navigator_state import NavigatorState

class ReturnBallState(NavigatorState):
    # 0.1 sec on a speed of 200 is ~15deg rotation
    # 0.2 sec on a speed of 200 is ~22deg rotation
    # 2 sec on a speed of 150 is ~90 deg rotation
    speed = 200
    turning_speed = 150

    target_rotation = None

    rotation = None
    position = None

    steps_forward = 0
    
    def start(self):
        self.rotation = self.calculate_start_rotation()
        self.target_rotation = self.calculate_target_rotation()

    def update(self):
        if self.context.zones.at_collection():
            print("at collection")
            return

        self.target_rotation = self.calculate_target_rotation()

        rotation_difference = self.rotation - self.target_rotation
        distance = self.calculate_target_distance()

        if self.is_middle(rotation_difference):
            print("forward")
            self.context.zumo.run("move", self.speed)
            time.sleep(0.1)
            

        elif self.is_left(rotation_difference):
            rotation_angle = abs(rotation_difference)
            max_turn_radius = 90
            max_time_to_turn = 2

            required_time = (rotation_angle / max_turn_radius) * 2

            time_to_turn = min(required_time, max_time_to_turn)

            self.rotation -= min(rotation_difference, max_turn_radius)
            self.context.zumo.run("left", self.turning_speed)

            print("left: time to turn: %s, rot diff: %s" % (time_to_turn, rotation_difference))

            time.sleep(time_to_turn)

            self.context.zumo.run("stop ")
            time.sleep(0.1)

        elif self.is_right(rotation_difference):
            rotation_angle = abs(rotation_difference)
            max_turn_radius = 90
            max_time_to_turn = 2

            required_time = (rotation_angle / max_turn_radius) * 2

            time_to_turn = min(required_time, max_time_to_turn)

            self.rotation -= min(rotation_difference, max_turn_radius)
            self.context.zumo.run("right", self.turning_speed)

            print("right: time to turn: %s, rot diff: %s" % (time_to_turn, rotation_difference))

            time.sleep(time_to_turn)

            self.context.zumo.run("stop ")
            time.sleep(0.1)

        print((rotation_difference, distance, self.target_rotation, self.rotation))

    def is_middle(self, rotation: float) -> bool:
        return rotation >= -10 and rotation <= 10

    def is_right(self, rotation: float) -> bool:
        return rotation < -10

    def is_left(self, rotation: float) -> bool:
        return rotation > 10

    def slow_stop(self, steps: int, wait_time: float) -> None:
        for i in range(0, steps):
            current_speed = self.speed - ((self.speed / steps) * i)

            self.context.zumo.run("move", current_speed)
            time.sleep(wait_time / steps)

        self.context.zumo.run("stop")

    def calculate_target_distance(self) -> float:
        (beacon_x, beacon_y) = self.context.zones.selected_collection_position()
        (cart_x, cart_y) = self.context.scanner.cart_position()

        x = beacon_x - cart_x
        y = beacon_y - cart_y
        
        return math.sqrt(x ** 2 + y ** 2)
        
    def calculate_target_rotation(self) -> float:
        (x, y) = self.context.scanner.cart_position()
        return self.context.zones.selected_collection_rotation(x, y)

    def calculate_start_rotation(self) -> float:
        print("go")

        print(self.context.zumo)

        self.context.zumo.run("honk")

        # wait for beacons
        time.sleep(10)

        self.context.scanner.update_location()

        print("move")
        self.context.zumo.run("honk")

        self.context.zumo.run("move", self.speed)
        time.sleep(2)

        print("stop")
        self.slow_stop(10, 1)

        # wait for beacons
        time.sleep(10)

        self.context.scanner.update_location()

        self.context.zumo.run("honk")

        return self.context.scanner.cart_rotation()

    def calculate_rotation(self) -> float:
        self.context.scanner.update_location()
        return self.context.scanner.cart_rotation()
    
    def stop(self):
        pass