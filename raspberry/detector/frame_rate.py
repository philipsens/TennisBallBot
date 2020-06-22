import cv2


class FrameRate:
    frame_rate_calculation: int
    frequency: int
    start_time: int

    def __init__(self):
        self.frame_rate_calculation = 1
        self.frequency = cv2.getTickFrequency()

    def reset(self):
        self.start_time = cv2.getTickCount()

    def calculate(self):
        end_time = cv2.getTickCount()
        calculated_time = (end_time - self.start_time) / self.frequency
        self.frame_rate_calculation = 1 / calculated_time