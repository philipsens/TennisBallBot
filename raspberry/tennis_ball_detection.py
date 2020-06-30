import time

from detector.ObjectDetector import ObjectDetector
from zumo.zumo import Zumo

zumo = Zumo("/dev/ttyACM0")
zumo.start()

time.sleep(1)


def get_nearest_detection(detections):
    return max(detections, key=lambda detection: detection.width)


def get_ball(detections):

    ball = get_nearest_detection(detections)
    if ball.width < 1:
        if 0.4 < ball.position < 0.6:
            zumo.add('move', 150, 100)
            time.sleep(0.5)
        elif ball.position <= 0.4:
            zumo.add('left', 150, 50)
        elif ball.position >= 0.4:
            zumo.add('right', 150, 50)

    time.sleep(0.25)


ObjectDetector().start(get_ball)
