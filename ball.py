from entity import Entity
from config import Config
import pygame
import random

class Ball(Entity):
    def __init__(self, rackets, position, size = Config.BALL_SIZE, start_velocity = Config.BALL_START_VELOCITY, color = pygame.Color("white")):
        super().__init__()
        self.position = position
        self.size = size
        self.color = color
        self.start_velocity = start_velocity
        self.velocity = start_velocity
        self.rackets = rackets
        self.original_position = position

        # call self.reset() to randomize ball starting velocity
        self.reset()

        # event listener lists
        self.on_racket_hit = []
        self.on_boundary_hit = []

    def reset(self, randomize_velocity = True):        
        self.position = self.original_position
        vx, vy = self.start_velocity
        if randomize_velocity:
            if bool(random.getrandbits(1)):
                vx *= -1
            if bool(random.getrandbits(1)):
                vy *= -1
            vy *= (1 + random.random())
        self.velocity = (vx, vy)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], self.size, self.size))

    def update(self, delta):
        x = self.position[0] + self.velocity[0] * delta // 1000
        y = self.position[1] + self.velocity[1] * delta // 1000
        self.position = (x, y)
        self._handle_rackets()
        self._handle_boundaries()

    def _handle_rackets(self):        
        vx, vy = self.velocity
        ball_rect = (self.position[0], self.position[1], self.size, self.size)
        for racket in self.rackets:
            racket_rect = (racket.position[0], racket.position[1], racket.size[0], racket.size[1])
            if Ball._do_rects_intersect(ball_rect, racket_rect):
                # prevent the ball from getting stuck in the racket
                if vx < 0:
                    self.position = (racket.position[0] + racket.size[0], self.position[1])
                else:
                    self.position = (racket.position[0] - self.size, self.position[1])

                vx = -vx
                self.velocity = (vx, vy)
                self.racket_hit(racket) # trigger event        
        
    def _handle_boundaries(self):
        x, y = self.position
        vx, vy = self.velocity
        boundary = None
        if x < 0:
            x = -x
            vx = -self.velocity[0]
            boundary = "left"            
        elif x > Config.SCREENWIDTH - self.size:
            x = Config.SCREENWIDTH - self.size
            vx = -self.velocity[0]
            boundary = "right"
        elif y < 0:
            y = -y
            vy = -self.velocity[1]
            boundary = "top"
        elif y > Config.SCREENHEIGHT - self.size:
            y = Config.SCREENHEIGHT - self.size
            vy = -self.velocity[1]
            boundary = "bottom"            
        self.position = (x, y)
        self.velocity = (vx, vy)
        if boundary is not None:
            self.boundary_hit(boundary)

    def _do_rects_intersect(rect1, rect2):
        p1 = (rect1[0], rect1[1])
        p2 = (rect1[0] + rect1[2], rect1[1] + rect1[3])
        p3 = (rect2[0], rect2[1])
        p4 = (rect2[0] + rect2[2], rect2[1] + rect2[3])
        return p1[0] <= p4[0] and p2[0] >= p3[0] and p1[1] <= p4[1] and p2[1] >= p3[1]

    ################
    # event handling
    ################
    def _message_event_listeners(self, listeners_attribute_name, *args, **kwargs):
        ''' This method checks if there are event listeners that subscribed to the event which is
            passed in "listeners_attribute_name" and messages all the listeners.
            Example: _message_event_listeners("on_click", (100, 160)) will message all
                     listeners that subscribed to the "on_click" event and will pass (100, 160)
                     as argument.
        '''
        if hasattr(self, listeners_attribute_name):            
            # at least one listener has subscribed to this event
            # if listener attribute is no list -> convert to list
            if not type(getattr(self, listeners_attribute_name)) is list:
                setattr(self, listeners_attribute_name, [getattr(self, listeners_attribute_name)])                
            # message all listeners
            for listener in getattr(self, listeners_attribute_name):
                listener(self, *args, **kwargs)

    # ball events
    def racket_hit(self, racket):
        self._message_event_listeners("on_racket_hit", racket)

    def boundary_hit(self, boundary):
        self._message_event_listeners("on_boundary_hit", boundary)