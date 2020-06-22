from ObjectDetector import ObjectDetector


def get_nearest_detection(detections):
    print(max(detections, key=lambda detection: detection.width).position)


ObjectDetector().start(get_nearest_detection)
