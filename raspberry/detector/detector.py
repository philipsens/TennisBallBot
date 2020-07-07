import threading
import time

from simple_pid import PID

from .ObjectDetector import ObjectDetector
from zumo.zumo import Zumo


class Detector(threading.Thread):
    MIDDLE_POINT = 0.5
    CLOSE_POINT = 0.98
    MAX_SPEED = 300

    object_detector: ObjectDetector
    direction_pid: PID
    distance_pid: PID
    zumo: Zumo

    done_flag = False
    centered = False

    use_pid = bool

    def __init__(self, zumo, pid=False):
        threading.Thread.__init__(self)
        self.zumo = zumo
        self.use_pid = pid
        self.object_detector = ObjectDetector()

    def run(self):
        self.initialize_pid()
        self.object_detector.start(self.callback)

    def initialize_pid(self):
        self.direction_pid = PID(1, 0.1, 0.05, setpoint=self.MIDDLE_POINT)
        self.distance_pid = PID(1, 0.1, 0.05, setpoint=self.CLOSE_POINT)
        self.direction_pid.output_limits = (-0.5, 0.5)
        self.distance_pid.output_limits = (0, 1)

    def stop(self):
        self.object_detector.stop()

    def pause(self):
        self.object_detector.pause()

    def unpause(self):
        self.done_flag = False
        self.centered = False
        self.object_detector.unpause()

    def callback(self, detections):
        detection = self.get_nearest_detection(detections)
        
        if self.collected(detection):
            self.done()
            return

        if not self.centered:

            # [-1 = left & +1 = right]
            dir = (detection.position - .5) * 2

            left = dir < 0
            
            max_vision_radius = 30
            max_turn_radius = 120
            max_time_to_turn = 2

            angle_to_turn = abs(dir * max_vision_radius)

            required_time = (angle_to_turn / max_turn_radius) * max_time_to_turn
            time_to_turn = min(required_time, max_time_to_turn)

            if left:
                self.zumo.run("center-left", 200)
            else:

                self.zumo.run("center-right", 200)

            print(time_to_turn)

            time.sleep(time_to_turn)

            self.zumo.run("stop")
            self.zumo.run("honk")

            time.sleep(0.1)

            self.centered = True

        direction, distance = self.get_control(detection)
        left, right = self.get_speed(direction, distance)

        self.zumo.run('left', left)
        self.zumo.run('right', right)

    @staticmethod
    def get_nearest_detection(detections):
        detection = max(detections, key=lambda d: d.width)
        # print(("detection: ", detection.class_id, detection.position, detection.width))
        return detection

    def collected(self, detection):
        return detection.width > self.CLOSE_POINT

    def is_done(self) -> bool:
        return self.done_flag

    def done(self):
        self.done_flag = True
        print("Collected ball")
        
        self.slow_stop(10, 1)

    def get_control(self, detection):
        if self.use_pid:
            direction_control = self.direction_pid(detection.position)
            distance_control = self.distance_pid(detection.width)
        else:
            direction_control = detection.position - 0.5
            distance_control = 1 - detection.width
        # print(("controls's: ", direction_control, distance_control))
        return direction_control, distance_control

    def get_speed(self, direction, distance):
        
        base_speed = 50
        additional_speed = 250

        left_norm = self.MIDDLE_POINT - direction
        right_norm = self.MIDDLE_POINT + direction

        left = base_speed + (additional_speed * left_norm)
        right = base_speed + (additional_speed * right_norm)
        
        print((left, right))

        return left, right


    def slow_stop(self, steps: int, wait_time: float) -> None:
        for i in range(0, steps):
            current_speed = 150 - ((150 / steps) * i)

            self.zumo.run("move", current_speed)
            time.sleep(wait_time / steps)

        self.zumo.run("stop")
