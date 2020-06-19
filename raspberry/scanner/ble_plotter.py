import threading
import time
import random

import matplotlib
matplotlib.use('GTK3Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import scanner

class BLEPlotter(threading.Thread):
    scanner = None
    stop_thread = False

    figure = None
    axes = None

    def __init__(self, scanner):
        threading.Thread.__init__(self)
        self.scanner = scanner
        self.stop_thread = False


    def run(self):
        self.setup()

        while self.stop_thread == False:
            self.render()

    def setup(self) -> None:
        self.figure = plt.figure(figsize=(8,8), dpi=72)
        self.axes = plt.subplot(aspect='equal')
        self.axes.set_title('Beacon positions')
    
    def clear(self) -> None:
        self.axes.clear()

        self.axes.set_xlim(-100, 100)
        self.axes.set_ylim(-100, 100)

        plt.grid()


    def render(self) -> None:
        # Rendering this is still very slow
        # It might be possible to change this to a blip way of rendering
        # I tried it once, but wasnt quite succesful

        self.clear()

        for beacon in self.scanner.beacons:
            x = beacon.position[0]
            y = beacon.position[1]
            radius = plt.Circle((x, y), beacon.avg(), color="#20fcc1", alpha=0.5)
            marker = plt.Circle((x, y), 5, color="#ff0000")

            self.axes.add_artist(radius)
            self.axes.add_artist(marker)

        # Cart position
        (x, y) = self.scanner.cart_position()
        center = plt.Circle((x, y), 5, color="#000000")
        self.axes.add_artist(center)

        print("[BLEPlotter] New frame...")
        plt.pause(.0001)


    def stop(self):
        self.stop_thread = True
        self.join()
