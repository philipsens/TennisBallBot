from .navigator_state import NavigatorState


class Navigator:
    state: NavigatorState = None
    scanner = None
    detector = None
    zones = None
    zumo = None
    
    def __init__(self, scanner, detector, zones, zumo) -> None:
        self.scanner = scanner
        self.detector = detector
        self.zones = zones
        self.zumo = zumo

    def transition_to(self, state: NavigatorState) -> None:

        if not self.state is None:
            self.state.stop()

        state.context = self
        self.state = state

        self.state.start()

    def update(self) -> None:
        self.state.update()

