from entity import Entity
from abc import abstractmethod
from sound_manager import Sound_manager

class GUI_widget(Entity):
    ''' Abstract base class for all GUI widgets '''
    
    def __init__(self, position):
        super().__init__()
        self.position = position
        self.can_be_focussed = False
        self.has_focus = False
        self.tab_index = 0

        # empty event listener lists
        self.on_click = []
        self.on_mouse_enter = []
        self.on_mouse_leave = []
        self.on_get_focus = []
        self.on_lose_focus = []
        self.on_key_down = []

    @abstractmethod
    def get_size(self):
        pass

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

    # events that every widget can have
    def click(self):
        if str(type(self)) == "<class 'button_widget.Button_widget'>":
            Sound_manager.play("menu_select")
        self._message_event_listeners("on_click")

    def mouse_enter(self):
        self._message_event_listeners("on_mouse_enter")

    def mouse_leave(self):
        self._message_event_listeners("on_mouse_leave")

    def get_focus(self):
        self._message_event_listeners("on_get_focus")

    def lose_focus(self):
        self._message_event_listeners("on_lose_focus")

    def key_down(self, event):
        self._message_event_listeners("on_key_down", event)