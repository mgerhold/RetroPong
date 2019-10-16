from entity import Entity
import pygame

class GUI_group(Entity):
    def __init__(self):
        self.widgets = []
        self.focus = None
        self.mouse_pos = pygame.mouse.get_pos()

    def add(self, *widgets):
        last_tab_index = 0 if len(self.widgets) == 0 else self.widgets[-1].tab_index
        for widget in widgets:
            if widget.can_be_focussed:
                widget.tab_index = last_tab_index + 1                
                last_tab_index = widget.tab_index
            self.widgets.append(widget)     

    def draw(self, surface):
        for widget in self.widgets:
            widget.draw(surface)

    def update(self, delta):
        for widget in self.widgets:
            widget.update(delta)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for widget in self.widgets:
                if GUI_group._coords_inside_rect(pygame.mouse.get_pos(), widget.position + widget.get_size()):
                    # clicked inside widget -> dispatch click event
                    widget.click()
        elif event.type == pygame.MOUSEMOTION:
            for widget in self.widgets:
                if GUI_group._coords_inside_rect(pygame.mouse.get_pos(), widget.position + widget.get_size()):
                    # mouse is inside widget -> check if mouse already was in widget before
                    if not GUI_group._coords_inside_rect(self.mouse_pos, widget.position + widget.get_size()):
                        # mouse has just been moved inside widget -> dispatch mouse_enter event
                        if self.focus is not None and self.focus != widget:
                            # another widget currently has focus
                            self.focus.lose_focus()
                        widget.mouse_enter()
                        widget.get_focus()
                        self.focus = widget
                else:
                    # mouse is not inside widget -> check if mouse was inside widget before
                    if GUI_group._coords_inside_rect(self.mouse_pos, widget.position + widget.get_size()):
                        # mouse was inside widget before -> dispatch mouse_leave event
                        widget.mouse_leave()
                        widget.lose_focus()
                        if self.focus is not None and self.focus == widget:
                            self.focus = None
            self.mouse_pos = pygame.mouse.get_pos()
        elif event.type == pygame.KEYDOWN:
            # key pressed -> check for arrow keys for navigation
            if event.key == pygame.K_UP:
                self._step_through_tab_index(True)
            elif event.key == pygame.K_DOWN:
                self._step_through_tab_index()

            # in general: send all key events to the focussed widget itself
            if self.focus is not None:                
                self.focus.key_down(event)

    def _step_through_tab_index(self, backwards = False):
        if self.focus is not None:
            if backwards:
                new_tab_index = self._get_max_tab_index() if self.focus.tab_index == 1 else self.focus.tab_index - 1
            else:                
                new_tab_index = self._get_min_tab_index() if self.focus.tab_index == self._get_max_tab_index() else self.focus.tab_index + 1
            if self.focus.tab_index != new_tab_index:
                # tab index has changed
                self.focus.lose_focus() # dispatch lose_focus event
                self.focus = self._get_widget_by_tab_index(new_tab_index) # change focus
                self.focus.get_focus() # dispatch get_focus event
        else:
            if backwards:
                new_tab_index = self._get_max_tab_index()
            else:
                new_tab_index = self._get_min_tab_index()
            if new_tab_index is not None:
                self.focus = self._get_widget_by_tab_index(new_tab_index) # set focus
                self.focus.get_focus() # dispatch get_focus event

    def _coords_inside_rect(coords, rect):
        return coords[0] >= rect[0] and coords[0] <= rect[0] + rect[2] and coords[1] >= rect[1] and coords[1] <= rect[1] + rect[3]

    def _get_max_tab_index(self):
        if len(self.widgets) == 0:
            return None
        max = 0
        for widget in self.widgets:
            if widget.tab_index > max and widget.can_be_focussed:
                max = widget.tab_index
        return None if max == 0 else max

    def _get_min_tab_index(self):
        if len(self.widgets) == 0:
            return None
        min = None
        for widget in self.widgets:
            if widget.can_be_focussed and (min is None or widget.tab_index < min):
                min = widget.tab_index
        return None if min == 0 else min

    def _get_widget_by_tab_index(self, tab_index):
        for widget in self.widgets:
            if widget.tab_index == tab_index:
                return widget
        return None