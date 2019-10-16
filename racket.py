from entity import Entity
from config import Config
import pygame

class Racket(Entity):
    def __init__(self, position, size, color = pygame.Color("white"), max_speed = Config.RACKET_SPEED):
        super().__init__()
        self.position = position
        self.size = size        
        self.color = color
        self.max_speed = max_speed
        self.movement = 0
        self.original_position = position

    def reset(self):
        self.position = self.original_position
        self.movement = 0

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1]))

    def steer(self, direction, max = None):
        if max is None:
            max = self.max_speed
        if direction == "up":
            self.movement = -min(self.max_speed, max)
        elif direction == "down":
            self.movement = min(self.max_speed, max)
        else:
            self.movement = 0

    def update(self, delta):
        y = self.position[1]
        y += self.movement * delta // 1000
        if y < 0:
            y = 0
        elif y > Config.SCREENHEIGHT - Config.RACKET_HEIGHT:
            y = Config.SCREENHEIGHT - Config.RACKET_HEIGHT
        self.position = (self.position[0], y)        