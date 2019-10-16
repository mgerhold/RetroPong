from entity import Entity
import importlib
import sys

class Gamestate_manager(Entity):
    def __init__(self):        
        self.current_gamestate = None        

    def change_gamestate(self, name):
        if self.current_gamestate is not None:
            self.current_gamestate.cleanup()
        module = importlib.import_module(name)
        class_ = getattr(module, name.capitalize())
        self.current_gamestate = class_()

    def draw(self, surface):
        if self.current_gamestate is not None:
            self.current_gamestate.draw(surface)

    def update(self, delta):
        next_gamestate = None
        if self.current_gamestate is not None:
            next_gamestate = self.current_gamestate.update(delta)
        if next_gamestate is not None and next_gamestate != "exit" and next_gamestate != self.current_gamestate.name:            
            self.change_gamestate(next_gamestate)
        return next_gamestate != "exit"

    def handle_event(self, event):
        if self.current_gamestate is not None:
            self.current_gamestate.handle_event(event)

    def _get_gamestate_by_name(self, name):
        for gamestate in self.gamestates:
            if gamestate.name == name:
                return gamestate
        return None