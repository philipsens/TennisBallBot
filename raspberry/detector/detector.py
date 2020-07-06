import threading

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
        self.object_detector.unpause()

    def callback(self, detections):
        detection = self.get_nearest_detection(detections)

        if self.collected(detection):
            self.done()
            return

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

    def done(self):
        self.zumo.run('stop')
        self.pause()
        print("Collected ball")

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
        speed = abs(max(distance * self.MAX_SPEED, 150))
        left = abs(self.MIDDLE_POINT - direction) * speed
        right = abs(self.MIDDLE_POINT + direction) * speed
        # print(("speeds's: ", speed, left, right))
        return left, right
