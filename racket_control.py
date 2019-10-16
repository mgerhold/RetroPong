from abc import ABC, abstractmethod

class Racket_control(ABC):
    def __init__(self, racket):
        super().__init__()
        self.racket = racket

    @abstractmethod
    def update(self, delta):
        pass