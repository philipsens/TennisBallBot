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


class Zumo(threading.Thread):
    queue = Queue()

    running = True
    serial_connection = None

    def __init__(self, port: str) -> None:
        threading.Thread.__init__(self)
        self.serial_connection = serial.Serial(port, 115200)

    def add(self, identifier: str, value: int = 0, time: int = 0) -> None:
        self.queue.put((identifier, value, time))

    def run(self):
        if not self.serial_connection.is_open:
            print("Cannot open serial connection")
            return

        while self.running:
            if self.queue.empty():
                time.sleep(0.25)
                continue

            message = self.compose_message()

            print(message)

            self.serial_connection.write(bytes(message, encoding="ascii"))

    def compose_message(self) -> str:
        messages = []

        while not self.queue.empty():
            identifier, value, time = self.queue.get()

            message = identifier + "=" + str(value) + "=" + str(time)
            messages.append(message)

        formatted_messages = ';'.join(messages) + "\r\n"

        return formatted_messages

    def stop(self) -> None:
        self.running = False
        self.join()
        self.serial_connection.close()
