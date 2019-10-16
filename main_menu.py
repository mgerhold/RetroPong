from gamestate import Gamestate
from gui_group import GUI_group
from text_widget import Text_widget
from button_widget import Button_widget
from config import Config
from sound_manager import Sound_manager
import pygame
import math
import random
import os

class Main_menu(Gamestate):
    def __init__(self):
        super().__init__("main_menu")
        self.gui = GUI_group()        

        splash_text = Text_widget(
            (Config.SCREENWIDTH // 2, Config.SCREENHEIGHT // 4 + 60),
            random.choice(Main_menu.SPLASH_TEXTS),
            color_normal=pygame.Color(180, 180, 180),
            text_justify="center",
            vertical_align="center"
        )

        start_button = Button_widget((Config.SCREENWIDTH // 2 - 125, Config.SCREENHEIGHT // 2), "Spiel starten")
        start_button.on_click.append(self.start_button_click)

        settings_button = Button_widget((Config.SCREENWIDTH // 2 - 125, Config.SCREENHEIGHT // 2 + 60), "Einstellungen")
        settings_button.on_click.append(self.settings_button_click)

        exit_button = Button_widget((Config.SCREENWIDTH // 2 - 125, Config.SCREENHEIGHT // 2 + 120), "Beenden")
        exit_button.on_click.append(self.exit_button_click)

        self.gui.add(splash_text, start_button, settings_button, exit_button)

        self.next_gamestate = None

        self.logo = pygame.image.load("logo.png")

        Sound_manager.stop_music()

    def draw(self, surface):
        self.gui.draw(surface)
        logo_scaled = pygame.transform.scale(self.logo, (round(self.logo.get_size()[0] * (math.sin(pygame.time.get_ticks() / 750) + 5) / 6), self.logo.get_size()[1]))
        surface.blit(logo_scaled, (Config.SCREENWIDTH // 2 - logo_scaled.get_size()[0] // 2, Config.SCREENHEIGHT // 4))

    def update(self, delta):
        self.gui.update(delta)
        return self.next_gamestate

    def handle_event(self, event):
        self.gui.handle_event(event)

    def cleanup(self):
        pass

    # events
    def start_button_click(self, sender):
        self.next_gamestate = 'game'

    def settings_button_click(self, sender):
        self.next_gamestate = 'settings_menu'

    def exit_button_click(self, sender):
        self.next_gamestate = 'exit'

    # load splash texts from "splashes.txt"
    filename = "splashes.txt"
    if os.path.isfile(filename):
        with open(filename, encoding="utf-8") as f:
            SPLASH_TEXTS = f.readlines()
        SPLASH_TEXTS = [line.strip() for line in SPLASH_TEXTS if len(line.strip()) <= 45]
    else:
        SPLASH_TEXTS = [f"<{filename} missing>"]