from typing import Tuple

class BLEBeacon:
    position: Tuple[int, int]
    results: []
    index = 0
    max_len = 0

    def calculate_distance(rssi: int, tx_power: int) -> float:
        return (10 ** ((tx_power - rssi) / (10 * 1.75))) * 10


    def calculate_accuracy(rssi: int, tx_power: int) -> float:
        if (rssi == 0):
            return -1
        
        ratio = rssi / tx_power

        if ratio < 1:
            return ratio ** 10
        else:
            return 0.89976 * (ratio ** 7.7095) + 0.111

    def __init__(self, max_len: int, position: Tuple[int, int]) -> None:
        # Preallocate the array for faster inserts
        self.results = max_len * [0]
        self.max_len = max_len
        self.position = position

    def push(self, value: float) -> None:
        key = (self.index + 1) % self.max_len
        self.index = key

        self.results[self.index] = value

    def avg(self) -> float:
        sum_results = sum(self.results)
        return sum_results / self.max_len
