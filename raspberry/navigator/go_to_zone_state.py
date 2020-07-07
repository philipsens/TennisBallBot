import math
import time
import navigator.navigator_state as NS
import navigator.search_ball_state as SBS

class GoToZoneState(NS.NavigatorState):

    rotation = 0
    target_rotation = 0
    

    def __init__(self, current_rotation: float):
        self.rotation = current_rotation
        pass 
    
    def start(self):
        self.target_rotation = self.calculate_target_rotation()

    def update(self):
        if self.context.zone.in_zone():
            print("in zone")
            time.sleep(1)

            self.context.transition_to(SBS.SearchBallState())

            return

        self.target_rotation = self.calculate_target_rotation()

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

            time_to_turn = min(required_time, max_time_to_turn)

            self.rotation -= min(rotation_difference, max_turn_radius)
            self.context.zumo.run("left", self.turning_speed)

            print("left: time to turn: %s, rot diff: %s" % (time_to_turn, rotation_difference))

            time.sleep(time_to_turn)

            self.slow_stop(5, 0.1)

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

            self.slow_stop(5, 0.1)
    
    def is_middle(self, rotation: float) -> bool:
        return rotation >= -5 and rotation <= 5

    def is_right(self, rotation: float) -> bool:
        return rotation < -5

    def is_left(self, rotation: float) -> bool:
        return rotation > 5

    def stop(self):
        pass

    def calculate_target_rotation(self):
        (x, y) = self.context.scanner.cart_position()
        return self.context.zones.selected_zone_rotation(x, y)