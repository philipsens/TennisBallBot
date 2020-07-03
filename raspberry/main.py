from scanner.scanner import BLEScanner
from plotter.plotter import Plotter
from zumo.zumo import Zumo
from webserver.webserver import Webserver
from zones.zones import Zones
from detector.detector import Detector
from navigator.navigator import Navigator
from navigator.return_ball_state import ReturnBallState

import time

if __name__ == '__main__':
    print("Starting TennisBallBot 🤖")

    zumo = Zumo("/dev/ttyACM0")
    scanner = BLEScanner("00000000-0000-0000-0000-000000000000")
    detector = Detector()
    webserver = Webserver("0.0.0.0")
    zones = Zones(webserver, scanner)

    navigator = Navigator(scanner, detector, zones, zumo)
    plotter = Plotter(scanner, zones)

    try:
        plotter.start()
        scanner.start()
        detector.start()
        webserver.start()

        navigator.transition_to(ReturnBallState())

        while True:
            navigator.update()

    except KeyboardInterrupt:
        plotter.stop()
        scanner.stop()
        detector.stop()
        webserver.stop()
