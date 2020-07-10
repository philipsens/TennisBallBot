import navigator.navigator_state as NS
import navigator.return_ball_state as RBS

class SearchBallState(NS.NavigatorState):
    
    def start(self):
        self.context.detector.unpause()
        print("search ball state")

    def update(self):
        if self.context.detector.is_done():
            self.context.transition_to(RBS.ReturnBallState())

    def stop(self):
        self.context.detector.pause()
