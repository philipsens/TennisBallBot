import importlib.util
import os
import time
from importlib import import_module
from threading import Thread

import cv2
import numpy as np


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


class Model:
    input_mean = 127.5
    input_std = 127.5

    labels: any
    interpreter: any

    input_details: any
    output_details: any
    height: any
    width: any
    floating_model: bool
    input_data: any

    def __init__(self, path_to_labels, path_to_graph):
        self.load_labels(path_to_labels)
        self.remove_coco_placeholder_label()
        self.load_graph(path_to_graph)
        self.load_model_details()
        self.check_floating_model()

    def load_labels(self, path_to_labels):
        with open(path_to_labels, 'r') as file:
            self.labels = [line.strip() for line in file.readlines()]

    def remove_coco_placeholder_label(self):
        if self.labels[0] == '???':
            del (self.labels[0])

    def load_graph(self, path_to_graph):
        tflite_runtime = self.get_tflite_runtime()
        self.interpreter = tflite_runtime.Interpreter(model_path=path_to_graph, experimental_delegates=[
            tflite_runtime.load_delegate('libedgetpu.so.1.0')])
        self.interpreter.allocate_tensors()

    @staticmethod
    def get_tflite_runtime():
        pkg = importlib.util.find_spec('tflite_runtime')
        if pkg:
            return import_module('tflite_runtime.interpreter')
        else:
            return import_module('tensorflow.lite.python.interpreter')

    def load_model_details(self):
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.height = self.input_details[0]['shape'][1]
        self.width = self.input_details[0]['shape'][2]

    def check_floating_model(self):
        self.floating_model = (self.input_details[0]['dtype'] == np.float32)

    def create_input_data_from_frame(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (self.width, self.height))
        self.input_data = np.expand_dims(frame_resized, axis=0)
        self.normalize_pixel_values()

    def normalize_pixel_values(self):
        if self.floating_model:
            self.input_data = (np.float32(self.input_data) - self.input_mean) / self.input_std

    def run(self):
        self.interpreter.set_tensor(self.input_details[0]['index'], self.input_data)
        self.interpreter.invoke()

    def get_detection_results(self):
        boxes = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        classes = self.interpreter.get_tensor(self.output_details[1]['index'])[0]
        scores = self.interpreter.get_tensor(self.output_details[2]['index'])[0]
        return boxes, classes, scores


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


class Detection:
    boxes: []
    class_id: int
    score: float
    width: float
    position: float

    def __init__(self, boxes, class_id, score):
        self.boxes = boxes
        self.class_id = class_id
        self.score = score
        self.width, self.position = self.get_width_and_position(boxes)

    @staticmethod
    def get_width_and_position(boxes):
        xmin = boxes[1]
        xmax = boxes[3]

        width = (xmax - xmin)
        position = xmin + (width / 2)

        return width, position


class ObjectDetector:
    MODEL_DIR = 'TFLite_model'
    GRAPH_NAME = 'edgetpu.tflite'
    LABELMAP_NAME = 'labelmap.txt'
    MIN_CONFIDENCE_THRESHOLD = 0.5
    RESOLUTION_WIDTH = 1280
    RESOLUTION_HEIGHT = 720

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
        while self.running:
            # self.frame_rate.reset()

            frame = self.video_stream.read().copy()
            self.model.create_input_data_from_frame(frame)
            self.model.run()
            boxes, classes, scores = self.model.get_detection_results()

            detections = self.get_confident_detections(boxes, classes, scores)

            if callback and detections:
                callback(detections)
            elif detections:
                print(detections)

            # self.frame_rate.calculate()
            # print(self.frame_rate.frame_rate_calculation)

        self.video_stream.stop()

    def get_confident_detections(self, boxes, classes, scores):
        detections = []
        for i in range(len(scores)):
            if (scores[i] > self.MIN_CONFIDENCE_THRESHOLD) and (scores[i] <= 1.0):
                detections.append(Detection(boxes[i], classes[i], scores[i]))
        return detections

    def stop(self):
        self.running = False


def get_nearest_detection(detections):
    print(max(detections, key=lambda detection: detection.width).position)


ObjectDetector().start(get_nearest_detection)
