from gui_widget import GUI_widget
import pygame
from globals import Globals

class Text_widget(GUI_widget):

    def __init__(
            self,
            position,
            text,
            color_normal = pygame.Color("white"),
            color_focussed = pygame.Color("white"),
            background_color = None,
            text_justify = "left",
            vertical_align = "bottom"
        ):
        super().__init__(position)
        self.text = text
        self.color = color_normal
        self.color_normal = color_normal
        self.color_focussed = color_focussed
        self.background_color = background_color
        self.text_justify = text_justify
        self.vertical_align = vertical_align

        self.on_mouse_enter = [self._text_mouse_enter]
        self.on_mouse_leave = [self._text_mouse_leave]
        self.on_get_focus = [self._text_get_focus]
        self.on_lose_focus = [self._text_lose_focus]

    def draw(self, surface):        
        font = Globals.font
        text_surface = font.render(self.text, False, self.color, self.background_color)
        position = [self.position[0], self.position[1]]
        if self.text_justify == "center":
            position[0] = position[0] - text_surface.get_width() // 2
        elif self.text_justify == "right":
            position[0] = position[0] - text_surface.get_width()
        if self.vertical_align == "center":
            position[1] = position[1] - text_surface.get_height() // 2
        elif self.vertical_align == "top":
            position[1] = position[1] - text_surface.get_height()
        surface.blit(text_surface, (position[0], position[1]))

    def get_size(self):
        return Globals.font.size(self.text)

    def update(self, delta):        
        pass

    # event listeners for default mouse hover behavior
    def _text_mouse_enter(self, sender):
        self.get_focus()

    def _text_mouse_leave(self, sender):
        self.lose_focus()

    def _text_get_focus(self, sender):
        if self.can_be_focussed:
            self.color = self.color_focussed

    def _text_lose_focus(self, sender):
        if self.can_be_focussed:
            self.color = self.color_normal