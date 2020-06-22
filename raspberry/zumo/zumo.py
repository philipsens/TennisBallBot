import threading
import serial
import time
from queue import Queue

class Zumo(threading.Thread):

    queue = Queue()

    stop_thread = False
    serial_connection = None

    def __init__(self, port: str) -> None:
        threading.Thread.__init__(self)
        self.serial_connection = serial.Serial(port, 115200)

    def add(self, identifier: str, value: int) -> None:
        self.queue.put((identifier, value))

    def run(self):
        if (not self.serial_connection.is_open):
            print("Cannot open serial connection")
            return

        while self.stop_thread == False:
            if (self.queue.empty()):
                time.sleep(0.25)
                continue

            message = self.compose_message()

            print(message)

            self.serial_connection.write(bytes(message, encoding="ascii"))

    def compose_message(self) -> str:
        messages = []

        while not self.queue.empty():
            identifier, value = self.queue.get()

            message = identifier + "=" + str(value)
            messages.append(message)

        return ';'.join(messages) + "\r\n"

    def stop(self) -> None:
        self.stop_thread = True
        self.join()
        self.serial_connection.close()

    