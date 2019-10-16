from racket_control import Racket_control
import pygame

class Control_mouse(Racket_control):
    def update(self, delta):
        mouse_y = pygame.mouse.get_pos()[1]
        racket_y = self.racket.position[1] + self.racket.size[1] // 2
        
        if abs(racket_y - mouse_y) <= 3:
            # this prevents small and quick racket movements
            self.racket.steer(None)
        else:
            if racket_y < mouse_y:
                self.racket.steer("down", abs(racket_y - mouse_y) * 1000 / delta)
            elif racket_y > mouse_y:
                self.racket.steer("up", abs(racket_y - mouse_y) * 1000 / delta)
            else:
                self.racket.steer(None)