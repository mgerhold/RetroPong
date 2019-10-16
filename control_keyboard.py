from racket_control import Racket_control
import pygame

class Control_keyboard(Racket_control):
    def update(self, delta):
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.racket.steer("down")
        elif pygame.key.get_pressed()[pygame.K_UP]:
            self.racket.steer("up")
        else:
            self.racket.steer(None)