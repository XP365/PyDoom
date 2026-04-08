import sys

class GameManager:
    def __init__(self):
        self.frameCap = 240
        return
    
    def gameShutdown(self, exitcode):
        print("Window Closed! Shutting Down.")
        sys.exit(exitcode)



gameManager = GameManager()