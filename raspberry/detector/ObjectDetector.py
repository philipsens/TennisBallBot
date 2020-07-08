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
    RESOLUTION_WIDTH = 480
    RESOLUTION_HEIGHT = 360

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

            detections = []
            for i in range(len(scores)):
                if (scores[i] > self.MIN_CONFIDENCE_THRESHOLD) and (scores[i] <= 1.0):
                    detections.append(Detection(boxes[i], classes[i], scores[i]))

                    ymin = int(max(1, (boxes[i][0] * self.RESOLUTION_HEIGHT)))
                    xmin = int(max(1, (boxes[i][1] * self.RESOLUTION_WIDTH)))
                    ymax = int(min(self.RESOLUTION_HEIGHT, (boxes[i][2] * self.RESOLUTION_HEIGHT)))
                    xmax = int(min(self.RESOLUTION_WIDTH, (boxes[i][3] * self.RESOLUTION_WIDTH)))

                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (10, 255, 0), 2)

                    # Draw label
                    object_name = self.model.labels[int(classes[i])]  # Look up object name from "labels" array using class index
                    label = '%s: %d%%' % (object_name, int(scores[i] * 100))  # Example: 'person: 72%'
                    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)  # Get font size
                    label_ymin = max(ymin, labelSize[1] + 10)  # Make sure not to draw label too close to top of window
                    cv2.rectangle(frame, (xmin, label_ymin - labelSize[1] - 10),
                                  (xmin + labelSize[0], label_ymin + baseLine - 10), (255, 255, 255),
                                  cv2.FILLED)  # Draw white box to put label text in
                    cv2.putText(frame, label, (xmin, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0),
                                2)  # Draw label text

            # Draw framerate in corner of frame
            cv2.putText(frame, 'FPS: {0:.2f}'.format(self.frame_rate.frame_rate_calculation), (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (255, 255, 0), 2, cv2.LINE_AA)

            cv2.imshow('Object detector', frame)

            if cv2.waitKey(1) == ord('q'):
                break

            if callback and detections:
                callback(detections)
            elif detections:
                print(detections)

            self.frame_rate.calculate()

        self.video_stream.stop()

    def stop(self):
        self.running = False


    def pause(self):
        print("ObjectDetector paused")
        self.paused = True


    def unpause(self):
        print("ObjectDetector unpaused")
        self.paused = False
