import os
import time

import cv2

from .Detection import Detection
from .FrameRate import FrameRate
from .Model import Model
from .VideoStream import VideoStream


class ObjectDetector:
    MODEL_DIR = 'detector/TFLite_model'
    GRAPH_NAME = 'edgetpu.tflite'
    LABELMAP_NAME = 'labelmap.txt'
    MIN_CONFIDENCE_THRESHOLD = 0.5
    RESOLUTION_WIDTH = 1280
    RESOLUTION_HEIGHT = 720

    paused = True
    running = True

    video_stream: VideoStream
    frame_rate: FrameRate
    model: Model

    def __init__(self):
        path_to_labels, path_to_graph = self.get_file_paths()
        self.model = Model(path_to_labels, path_to_graph)

    def get_file_paths(self):
        current_working_directory = os.getcwd()
        path_to_labels = os.path.join(current_working_directory, self.MODEL_DIR, self.LABELMAP_NAME)
        path_to_graph = os.path.join(current_working_directory, self.MODEL_DIR, self.GRAPH_NAME)
        return path_to_labels, path_to_graph

    def start(self, callback=None):
        self.frame_rate = FrameRate()
        self.initialize_video_stream()
        self.update(callback)

    def initialize_video_stream(self):
        self.video_stream = VideoStream(resolution=(self.RESOLUTION_WIDTH, self.RESOLUTION_HEIGHT)).start()
        time.sleep(1)

    def update(self, callback):
        out = cv2.VideoWriter('output.avi', -1, 20.0, (640, 480))

        while self.running:
            self.frame_rate.reset()

            # if paused, just sleep and check again
            if self.paused:
                time.sleep(0.25)
                continue

            frame = self.video_stream.read().copy()
            self.model.create_input_data_from_frame(frame)
            self.model.run()
            boxes, classes, scores = self.model.get_detection_results()

            detections = self.get_confident_detections(boxes, classes, scores)

            cv2.imshow('Object detector', frame)
            out.write(frame)

            if cv2.waitKey(1) == ord('q'):
                break

            if callback and detections:
                callback(detections)
            elif detections:
                print(detections)


            self.frame_rate.calculate()
            print(self.frame_rate.frame_rate_calculation)

        self.video_stream.stop()

    def get_confident_detections(self, boxes, classes, scores):
        detections = []
        for i in range(len(scores)):
            if (scores[i] > self.MIN_CONFIDENCE_THRESHOLD) and (scores[i] <= 1.0):
                detections.append(Detection(boxes[i], classes[i], scores[i]))
        return detections

    def stop(self):
        self.running = False


    def pause(self):
        print("ObjectDetector paused")
        self.paused = True


    def unpause(self):
        print("ObjectDetector unpaused")
        self.paused = False
