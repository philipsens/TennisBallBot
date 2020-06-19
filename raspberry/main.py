from scanner.ble_scanner import BLEScanner
from scanner.ble_plotter import BLEPlotter
from zumo.zumo import Zumo
from main_thread.main_thread_queue import MainThreadQueue

if __name__ == '__main__':
    print("Starting TennisBallBot 🤖")

    queue = MainThreadQueue()

    scanner = BLEScanner("00000000-0000-0000-0000-000000000000")
    plotter = BLEPlotter(scanner)
    # zumo = Zumo()

    try:
        plotter.start()
        scanner.start()
        # zumo.start()

        while True:
            queue.execute()

    except KeyboardInterrupt:
        plotter.stop()
        scanner.stop()
        # zumo.stop()
