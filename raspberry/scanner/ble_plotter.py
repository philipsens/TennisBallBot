import threading
import time
import random


import pygame
import scanner

class BLEPlotter(threading.Thread):
    scanner = None
    stop_thread = False

    screen = None

    # screen dimensions are 500px x 500px
    screen_dimensions = (500, 500)
    # Field is 150cm x 150cm
    field = (150, 150)

    # pixel ratio
    ratio = None
    ratio_x = None
    ratio_y = None

    center = None

    def __init__(self, scanner):
        threading.Thread.__init__(self)
        self.scanner = scanner
        self.stop_thread = False


    def run(self):
        self.setup()

        while self.stop_thread == False:
            self.render()

    def setup(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_dimensions, 0, 32)
        pygame.display.set_caption("Plotter")

        self.ratio = self.ratio_x, self.ratio_y = (self.screen_dimensions[0] / self.field[0], self.screen_dimensions[1] / self.field[1])
        self.center = (self.screen_dimensions[0] // 2, self.screen_dimensions[1] // 2)
    
    def clear(self) -> None:
        self.screen.fill((255, 255, 255))

    def render(self) -> None:
        self.clear()

        for beacon in self.scanner.beacons:
            x = self.center[0] + int(beacon.position[0] * self.ratio_x)
            y = self.center[1] + int(beacon.position[1] * self.ratio_y)

            # radius
            surface = pygame.Surface(self.screen_dimensions)
            surface.set_colorkey((0,0,0))
            surface.set_alpha(128)

            pygame.draw.circle(surface, (0, 0, 255), (x, y), int(beacon.avg() * self.ratio_x))

            self.screen.blit(surface, (0, 0))

            # beacon
            pygame.draw.circle(self.screen, (255, 0, 0), (x, y), int(5 * self.ratio_x))

        (cart_x, cart_y) = self.scanner.cart_position()
        x = self.center[0] + int(cart_x * self.ratio_x)
        y = self.center[1] + int(cart_y * self.ratio_y)
        
        pygame.draw.circle(self.screen, (0, 0, 0), (x, y), int(5 * self.ratio_x))

        pygame.display.update()

        time.sleep(0.25)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop_thread = True

    def stop(self):
        self.stop_thread = True
        self.join()
