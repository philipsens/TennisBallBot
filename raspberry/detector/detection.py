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