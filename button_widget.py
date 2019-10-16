from gui_widget import GUI_widget
from text_widget import Text_widget
from sound_manager import Sound_manager
import pygame

class Button_widget(GUI_widget):

    def __init__(
            self,
            position,
            text,
            color_normal = pygame.Color(180, 180, 180),
            color_focussed = pygame.Color("white"),
            button_color = pygame.Color(40, 40, 40),
            size = (250, 45)):

        super().__init__(position)

        self.text_widget = Text_widget([position[0] + size[0] // 2, position[1] + size[1] // 2],
            text,
            color_normal,
            text_justify="center",
            vertical_align="center"
        )     

        self.color_normal = color_normal
        self.color_focussed = color_focussed
        self.button_color = button_color
        self.size = size
        self.can_be_focussed = True
        self.on_mouse_enter = [self._button_mouse_enter]
        self.on_mouse_leave = [self._button_mouse_leave]
        self.on_get_focus = [self._button_get_focus]
        self.on_lose_focus = [self._button_lose_focus]
        self.on_key_down = [self._button_key_down]

    def draw(self, surface):
        pygame.draw.rect(surface, self.button_color, pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1]))
        self.text_widget.draw(surface)

    def get_size(self):
        return self.size
        
    def update(self, delta):
        pass

    # event listeners for default mouse hover behavior
    def _button_mouse_enter(self, sender):        
        self.text_widget.color = self.color_focussed

    def _button_mouse_leave(self, sender):        
        self.text_widget.color = self.color_normal

    def _button_get_focus(self, sender):
        self.text_widget.color = self.color_focussed
        Sound_manager.play("menu_move")

    def _button_lose_focus(self, sender):
        self.text_widget.color = self.color_normal

    # event listener for default behavior when pressing return
    def _button_key_down(self, sender, event):
        if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:            
            self.click()