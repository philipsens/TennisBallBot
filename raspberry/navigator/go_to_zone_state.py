import math
import time
import navigator.navigator_state as NS
import navigator.search_ball_state as SBS

class GoToZoneState(NS.NavigatorState):

    speed = 200
    turning_speed = 175

    target_rotation = 0

    rotation = 0
    position = (0, 0)
    last_command = None

    def __init__(self, current_rotation: float):
        self.rotation = current_rotation

        print("rotation: %s" % self.rotation)
        pass 
    
    def start(self):
        self.target_rotation = self.calculate_target_rotation()

    def update(self):
        if self.context.zones.in_zone():
            print("in zone")
            self.context.zumo.run("stop")

            time.sleep(1)
            self.context.transition_to(SBS.SearchBallState())
            return

        rotation_difference = self.rotation - self.target_rotation

        if self.is_middle(rotation_difference):
            print("forward")
            self.context.zumo.run("move", self.speed)
            time.sleep(0.1)

        elif self.is_left(rotation_difference):

            rotation_angle = abs(rotation_difference)
            max_turn_radius = 90
            max_time_to_turn = 2

            required_time = (rotation_angle / max_turn_radius) * 2
            angle_to_turn = min(rotation_angle, max_turn_radius)

            time_to_turn = min(required_time, max_time_to_turn)

            self.rotation -= rotation_angle
            self.context.zumo.run("left", self.turning_speed)

            print("left: time to turn: %s, rot diff: %s" % (time_to_turn, angle_to_turn))

            time.sleep(time_to_turn)

            self.context.zumo.run("left", 0)
            time.sleep(0.1)

            self.context.zumo.run("stop")
            time.sleep(0.25)

            self.target_rotation = self.calculate_target_rotation()

        elif self.is_right(rotation_difference):

            rotation_angle = abs(rotation_difference)
            max_turn_radius = 90
            max_time_to_turn = 2

            required_time = (rotation_angle / max_turn_radius) * 2
            angle_to_turn = min(rotation_angle, max_turn_radius)

            time_to_turn = min(required_time, max_time_to_turn)

            self.rotation += angle_to_turn
            self.context.zumo.run("right", self.turning_speed)

            print("right: time to turn: %s, rot diff: %s" % (time_to_turn, angle_to_turn))

            time.sleep(time_to_turn)

            self.context.zumo.run("right", 0)
            time.sleep(0.1)

            self.context.zumo.run("stop")
            time.sleep(0.25)

            self.target_rotation = self.calculate_target_rotation()

    
    def is_middle(self, rotation: float) -> bool:
        return rotation >= -5 and rotation <= 5

    def is_right(self, rotation: float) -> bool:
        return rotation < -5

    def is_left(self, rotation: float) -> bool:
        return rotation > 5

    def stop(self):
        pass

    def start_position(self) -> None:
        print("Waiting for position...")
        time.sleep(20)
        self.position = self.context.scanner.update_location()

    def calculate_target_rotation(self) -> float:
        return self.context.zones.selected_zone_rotation(
            self.position[0],
            self.position[1]
        )