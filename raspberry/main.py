from scanner.ble_scanner import BLEScanner
from plotter.plotter import Plotter
from zumo.zumo import Zumo

if __name__ == '__main__':
    print("Starting TennisBallBot 🤖")

    zumo = Zumo("/dev/ttyACM0")
    scanner = BLEScanner("00000000-0000-0000-0000-000000000000")
    plotter = Plotter(scanner)

    try:
        zumo.start()
        plotter.start()
        scanner.start()

        zumo.add("left") # max value = 400
        zumo.add("right") # max value = 400
        zumo.add("honk") # value is ignored

    except KeyboardInterrupt:
        zumo.stop()
        plotter.stop()
        scanner.stop()
