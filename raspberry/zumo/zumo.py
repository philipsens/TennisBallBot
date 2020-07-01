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

        with self.lock:
            if not self.serial_connection.is_open:
                print("Serial connection is closed")
                return

            while self.serial_connection.inWaiting() > 0:
                # Clear out buffer (else the Serial connection becomes really slow)
                self.serial_connection.read(1)

            message = identifier + "=" + str(value) + "=" + str(wait_time) + ";\r\n"

            self.serial_connection.write(bytes(message, encoding="ascii"))

            time.sleep(wait_time / 1000)
