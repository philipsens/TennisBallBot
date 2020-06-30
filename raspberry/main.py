from scanner.scanner import BLEScanner
from plotter.plotter import Plotter
from zumo.zumo import Zumo
from webserver.webserver import Webserver
from zones.zones import Zones

import time

if __name__ == '__main__':
    print("Starting TennisBallBot 🤖")

    zumo = Zumo("/dev/ttyACM0")
    scanner = BLEScanner("00000000-0000-0000-0000-000000000000")
    webserver = Webserver("0.0.0.0")
    zones = Zones(webserver, scanner)

    plotter = Plotter(scanner, zones)

    try:
        plotter.start()
        zumo.start()
        scanner.start()
        webserver.start()

    except KeyboardInterrupt:
        plotter.stop()
        webserver.stop()
        scanner.stop()
        zumo.stop()
