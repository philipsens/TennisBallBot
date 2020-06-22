import cv2
from threading import Thread


class VideoStream:
    running = True

    def __init__(self, resolution=(640, 480)):
        self.stream = cv2.VideoCapture(0)
        self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        self.stream.set(3, resolution[0])
        self.stream.set(4, resolution[1])
        (self.grabbed, self.frame) = self.stream.read()

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while self.running:
            (self.grabbed, self.frame) = self.stream.read()
        self.stream.release()

    def read(self):
        return self.frame

    def stop(self):
        self.running = False