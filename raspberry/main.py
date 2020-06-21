from scanner.ble_scanner import BLEScanner
from scanner.ble_plotter import BLEPlotter
from zumo.zumo import Zumo
from main_thread.main_thread_queue import MainThreadQueue

if __name__ == '__main__':
    print("Starting TennisBallBot 🤖")

    queue = MainThreadQueue()

    zumo = Zumo("/dev/ttyACM1")
    scanner = BLEScanner("00000000-0000-0000-0000-000000000000")
    plotter = BLEPlotter(scanner)

    try:
        zumo.start()
        plotter.start()
        scanner.start()

        zumo.add("left", 0) # max value = 400
        zumo.add("right", 0) # max value = 400
        zumo.add("honk", 0) # value is ignored

        while True:
            queue.execute()

    except KeyboardInterrupt:
        zumo.stop()
        plotter.stop()
        scanner.stop()
