from gamestate import Gamestate
from gui_group import GUI_group
from text_widget import Text_widget
from button_widget import Button_widget
from config import Config
from globals import Globals
from sound_manager import Sound_manager
import pygame

class Gameover(Gamestate):
    def __init__(self):
        super().__init__('gameover')

        self.next_gamestate = None

        self.gui = GUI_group()

        title = Text_widget((Config.SCREENWIDTH // 2, Config.SCREENHEIGHT // 4), "Ende des Spiels", text_justify="center", vertical_align="center")

        if not hasattr(Globals, "winner"):
            Globals.winner = "<?>"
        message = Text_widget((Config.SCREENWIDTH // 2, Config.SCREENHEIGHT // 2), f"Spieler {Globals.winner} hat gewonnen!", text_justify="center")

        btn_restart = Button_widget(
            (Config.SCREENWIDTH // 2 - 125, Config.SCREENHEIGHT - Config.MARGIN - 100),
            "Nochmal"
        )
        btn_restart.on_click.append(self.btn_restart_click)

        btn_menu = Button_widget(
            (Config.SCREENWIDTH // 2 - 125, Config.SCREENHEIGHT - Config.MARGIN - 45),
            "Hauptmenü"
        )
        btn_menu.on_click.append(self.btn_menu_click)

        self.gui.add(
            title,
            message,
            btn_restart,
            btn_menu
        )

        Sound_manager.play("gameover")

    def draw(self, surface):
        self.gui.draw(surface)

    def update(self, delta):
        self.gui.update(delta)
        return self.next_gamestate

    def cleanup(self):
        pass

    def handle_event(self, event):
        self.gui.handle_event(event)

    # events
    def btn_menu_click(self, sender):
        self.next_gamestate = "main_menu"

    def btn_restart_click(self, sender):
        self.next_gamestate = "game"