from scanner.scanner import BLEScanner
from plotter.plotter import Plotter
from zumo.zumo import Zumo
from webserver.webserver import Webserver

if __name__ == '__main__':
    print("Starting TennisBallBot 🤖")

    zumo = Zumo("/dev/ttyACM0")
    scanner = BLEScanner("00000000-0000-0000-0000-000000000000")
    plotter = Plotter(scanner)
    webserver = Webserver("0.0.0.0")

    try:
        zumo.start()
        plotter.start()
        scanner.start()
        webserver.start()

    except KeyboardInterrupt:
        zumo.stop()
        plotter.stop()
        scanner.stop()
        webserver.stop()
