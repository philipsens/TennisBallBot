import math
import time
import navigator.navigator_state as NS
import navigator.go_to_zone_state as GTZS

class ReturnBallState(NS.NavigatorState):
    # 0.1 sec on a speed of 200 is ~15deg rotation
    # 0.2 sec on a speed of 200 is ~22deg rotation
    # 2 sec on a speed of 150 is ~90 deg rotation
    speed = 220
    turning_speed = 150

    target_rotation = None

    rotation = None
    position = None
    last_command = None

    steps_forward = 0

    collection_counter = 0
    
    def start(self):
        self.rotation = self.calculate_start_rotation()
        self.target_rotation = self.calculate_target_rotation()

    def update(self):
        if self.context.zones.at_collection():
            self.collection_counter += 1
            print("at collection")

            self.context.zumo.run("stop")

            if self.collection_counter > 10:
               self.context.zumo.run("move", -self.speed)
 
               time.sleep(1.5)

               self.context.zumo.run("stop")
               self.context.transition_to(GTZS.GoToZoneState(self.rotation))

            return

        self.collection_counter = 0

        rotation_difference = self.rotation - self.target_rotation
        distance = self.calculate_target_distance()

        if self.is_middle(rotation_difference):
            print("forward")
            self.context.zumo.run("move", self.speed)
            self.last_command = "move"
            
            time.sleep(0.1)
            
            
        elif self.is_left(rotation_difference):

            if self.last_command == "move":
                self.slow_stop(10, 1)

            rotation_angle = abs(rotation_difference)
            max_turn_radius = 90
            max_time_to_turn = 2

            required_time = (rotation_angle / max_turn_radius) * 2
            angle_to_turn = min(rotation_angle, max_turn_radius)

            time_to_turn = min(required_time, max_time_to_turn)

            self.rotation -= rotation_angle
            self.context.zumo.run("left", self.turning_speed)
            self.last_command = "left"

            print("left: time to turn: %s, rot diff: %s" % (time_to_turn, angle_to_turn))

            time.sleep(time_to_turn)

            self.context.zumo.run("left", 0)
            time.sleep(0.1)

            self.context.zumo.run("stop")
            time.sleep(0.25)

            self.target_rotation = self.calculate_target_rotation()

        elif self.is_right(rotation_difference):

            if self.last_command == "move":
                self.slow_stop(10, 1)

            rotation_angle = abs(rotation_difference)
            max_turn_radius = 90
            max_time_to_turn = 2

            required_time = (rotation_angle / max_turn_radius) * 2
            angle_to_turn = min(rotation_angle, max_turn_radius)

            time_to_turn = min(required_time, max_time_to_turn)

            self.rotation += angle_to_turn
            self.context.zumo.run("right", self.turning_speed)
            self.last_command = "right"

            print("right: time to turn: %s, rot diff: %s" % (time_to_turn, angle_to_turn))

            time.sleep(time_to_turn)

            self.context.zumo.run("right", 0)
            time.sleep(0.1)

            self.context.zumo.run("stop")
            time.sleep(0.25)

            self.target_rotation = self.calculate_target_rotation()

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

        self.context.zumo.run("honk")

        # wait for beacons
        time.sleep(20)

        self.context.scanner.update_location()

        print("move")
        self.context.zumo.run("honk")

        self.context.zumo.run("move", self.speed)
        time.sleep(1.75)

        print("stop")
        self.slow_stop(10, 1)

        # wait for beacons
        time.sleep(20)

        self.context.scanner.update_location()

        self.context.zumo.run("honk")

        return self.context.scanner.cart_rotation()

    def calculate_rotation(self) -> float:
        self.context.scanner.update_location()
        return self.context.scanner.cart_rotation()
    
    def stop(self):
        pass