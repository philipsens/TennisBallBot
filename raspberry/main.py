from scanner.scanner import BLEScanner
from plotter.plotter import Plotter
from zumo.zumo import Zumo
from webserver.webserver import Webserver
from zones.zones import Zones
from detector.detector import Detector

import time

if __name__ == '__main__':
    print("Starting TennisBallBot 🤖")

    zumo = Zumo("/dev/ttyACM0")
    scanner = BLEScanner("00000000-0000-0000-0000-000000000000")
    detector = Detector(zumo)
    webserver = Webserver("0.0.0.0")
    zones = Zones(webserver, scanner)

    plotter = Plotter(scanner, zones)

    try:
        plotter.start()
        scanner.start()
        detector.start()
        webserver.start()

        # temp: Only to show off the detector working
        time.sleep(5)

        detector.unpause()

    except KeyboardInterrupt:
        zumo.run('stop')
        plotter.stop()
        scanner.stop()
        detector.stop()
        webserver.stop()
