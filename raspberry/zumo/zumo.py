import threading
import serial
import time
from queue import Queue


'''
The commands accepted by the Zumo are the following

Command     Range       Time in ms
------------------------------
move        [-400, 400] yes
left        [-400, 400] yes
ball-left   [-400, 400] yes
right       [-400, 400] yes
ball-right  [-400, 400] yes
honk        -           no
delay       -           yes
'''


class Zumo:
    running = True
    serial_connection = None

    lock = threading.Lock()

    def __init__(self, port: str) -> None:
        threading.Thread.__init__(self)
        self.serial_connection = serial.Serial(port, 115200)

    def run(self, identifier: str, value: int = 0, wait_time: int = 0) -> None:

        self.lock.acquire()

        if not self.serial_connection.is_open:
            print("Serial connection is closed")
            return

        message = identifier + "=" + str(value) + "=" + str(wait_time) + ";\r\n"

        self.serial_connection.write(bytes(message, encoding="ascii"))

        time.sleep(wait_time / 1000)
        self.lock.release()

