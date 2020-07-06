from .navigator_state import NavigatorState
from .return_ball_state import ReturnBallState

class SearchBallState(NavigatorState):
    
    def start(self):
        self.context.detector.unpause()

    def update(self):
        if self.context.detector.is_done():
            self.context.transition_to(ReturnBallState())

    def stop(self):
        self.context.detector.pause()
