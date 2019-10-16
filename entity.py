from abc import ABC, abstractmethod     # abc = Abstract Base Classes

class Entity(ABC):
    ''' abstract base class for all classes that can draw and/or update themselves '''

    def __init__(self):
        super().__init__()

    @abstractmethod
    def draw(self, surface):
        ''' abstract method for drawing the entity onto a pygame surface '''
        pass

    @abstractmethod
    def update(self, delta):
        ''' abstract method for updating the entity over a time duration given in "delta" as milliseconds '''
        pass