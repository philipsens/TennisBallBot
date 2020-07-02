import time

from simple_pid import PID
from detector.ObjectDetector import ObjectDetector
from zumo.zumo import Zumo

MIDDLE_POINT = 0.5
CLOSE_POINT = 0.98
MAX_SPEED = 300
USE_PID = False

zumo = Zumo("/dev/ttyACM0")
zumo.run('stop')

direction_pid = PID(1, 0.1, 0.05, setpoint=MIDDLE_POINT)
distance_pid = PID(1, 0.1, 0.05, setpoint=CLOSE_POINT)
direction_pid.output_limits = (-0.5, 0.5)
distance_pid.output_limits = (0, 1)


def get_detection(detections):
    detection = get_nearest_detection(detections)

    if detection.width > CLOSE_POINT:
        zumo.run('stop')

        print("done")
        return

    if USE_PID:
        direction_control = direction_pid(detection.position)
        distance_control = distance_pid(detection.width)
        print(("pid's: ", direction_control, distance_control))
    else:
        direction_control = detection.position - 0.5
        distance_control = 1 - detection.width
        print(("delta's: ", direction_control, distance_control))

    speed = abs(max(distance_control * MAX_SPEED, 150))
    speed_left = abs(MIDDLE_POINT - direction_control) * speed
    speed_right = abs(MIDDLE_POINT + direction_control) * speed
    print(("speeds's: ", speed, speed_left, speed_right))

    zumo.run('left', speed_left)
    zumo.run('right', speed_right)


def get_nearest_detection(detections):
    detection = max(detections, key=lambda d: d.width)
    print(("detection: ", detection.class_id, detection.position, detection.width))
    return detection

try:
    ObjectDetector().start(get_detection)
except KeyboardInterrupt:
    zumo.run('stop')
