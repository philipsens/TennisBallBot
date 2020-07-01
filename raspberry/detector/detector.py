import threading
from .ObjectDetector import ObjectDetector

class Detector(threading.Thread):

    object_detector = ObjectDetector()

    def __init__(self):
        threading.Thread.__init__(self)


    def run(self):
        self.object_detector.start(Detector.callback)


    def stop(self):
        self.object_detector.stop()


    def pause(self):
        self.object_detector.pause()


    def unpause(self):
        self.object_detector.unpause()


    def callback(detections):
        print(max(detections, key=lambda detection: detection.width).position)


