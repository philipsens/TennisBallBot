import importlib.util
from importlib import import_module

import cv2
import numpy as np


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
