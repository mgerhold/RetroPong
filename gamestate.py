from abc import abstractmethod
from entity import Entity

class Gamestate(Entity):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def handle_event(self, event):
        pass

    @abstractmethod
    def cleanup(self):
        pass