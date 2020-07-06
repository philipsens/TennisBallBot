from .navigator_state import NavigatorState

class SearchBallState(NavigatorState):
    
    def start(self):
        self.context.detector.unpause()

    def update(self):
        pass

    def stop(self):
        self.context.detector.pause()
