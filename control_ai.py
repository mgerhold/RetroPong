from racket_control import Racket_control
from config import Config
import pygame

class Control_ai(Racket_control):
    def __init__(self, racket, ball):
        super().__init__(racket)
        self.ball = ball

    def update(self, delta):
        # check if ball is approaching
        if (self.racket.position[0] - self.ball.position[0]) * self.ball.velocity[0] > 0:
            # calculate ball destination (not taking bounces into consideration)
            rx = self.racket.position[0] if self.racket.position[0] > self.ball.position[0] else self.racket.position[0] + self.racket.size[0]
            dest_y = (rx - self.ball.position[0] + self.ball.size // 2) * self.ball.velocity[1] // self.ball.velocity[0] + self.ball.position[1] + self.ball.size // 2
        else:
            # if ball is not approaching -> return to middle of screen
            dest_y = Config.SCREENHEIGHT // 2

        racket_y = self.racket.position[1] + self.racket.size[1] // 2

        if abs(dest_y - racket_y) > 2*self.ball.size: # this prevents the racket from stuttering
            if dest_y > racket_y:
                self.racket.steer("down")
            elif dest_y < racket_y:
                self.racket.steer("up")
        else:
            self.racket.steer(None)