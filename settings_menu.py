from gamestate import Gamestate
from gui_group import GUI_group
from text_widget import Text_widget
from button_widget import Button_widget
from config import Config
import pygame

class Settings_menu(Gamestate):
    CONTROL_CHOICES = [
        ("Mensch (Pfeiltasten)", "keyboard"),
        ("Mensch (Maus)", "mouse"),
        ("Computer", "ai")
    ]

    def __init__(self):
        super().__init__('settings_menu')

        self.next_gamestate = None

        self.gui = GUI_group()

        title = Text_widget((Config.SCREENWIDTH // 2, Config.SCREENHEIGHT // 4), "Einstellungen", text_justify="center", vertical_align="center")

        player1_text = Text_widget(
            (Config.SCREENWIDTH // 2, Config.SCREENHEIGHT // 2 - 90),
            "Steuerung für Spieler 1",
            color_normal=pygame.Color(180, 180, 180),            
            text_justify="center"
        )
        self.btn_player1 = Button_widget(
            (Config.SCREENWIDTH // 2 - 175, Config.SCREENHEIGHT // 2 - 50),
            Settings_menu._get_control_text(Config.controls[0]),
            size=(350, 45)
        )
        self.btn_player1.on_click.append(self.btn_control1_click)

        player2_text = Text_widget(
            (Config.SCREENWIDTH // 2, Config.SCREENHEIGHT // 2 + 5),
            "Steuerung für Spieler 2",
            color_normal=pygame.Color(180, 180, 180),            
            text_justify="center"
        )
        self.btn_player2 = Button_widget(
            (Config.SCREENWIDTH // 2 - 175, Config.SCREENHEIGHT // 2 + 45),
            Settings_menu._get_control_text(Config.controls[1]),
            size=(350, 45)
        )
        self.btn_player2.on_click.append(self.btn_control2_click)

        score_limit_text = Text_widget(
            (Config.SCREENWIDTH // 2, Config.SCREENHEIGHT // 2 + 100),
            "Punkte-Ziel",
            color_normal=pygame.Color(180, 180, 180),
            text_justify="center"
        )
        btn_score_limit = Button_widget(
            (Config.SCREENWIDTH // 2 - 50, Config.SCREENHEIGHT // 2 + 140),
            str(Config.score_limit),
            size=(100, 45)
        )
        btn_score_limit.on_click.append(self.btn_score_limit_click)

        btn_ok = Button_widget(
            (Config.SCREENWIDTH // 2 - 125, Config.SCREENHEIGHT - Config.MARGIN - 45),
            "Speichern"
        )
        btn_ok.on_click.append(self.btn_ok_click)

        self.gui.add(
            title,
            player1_text,
            self.btn_player1,
            player2_text,
            self.btn_player2,
            score_limit_text,
            btn_score_limit,
            btn_ok
        )

    def _get_control_text(control_string):
        for element in Settings_menu.CONTROL_CHOICES:
            if element[1] == control_string:
                return element[0]
        return None

    def draw(self, surface):
        self.gui.draw(surface)

    def update(self, delta):
        self.btn_player1.color_normal = pygame.Color(200, 50, 50) if self.btn_player1.text_widget.text == self.btn_player2.text_widget.text else self.btn_player1.text_widget.color_normal
        if self.btn_player1.color_normal != self.btn_player1.text_widget.color and self.btn_player1.color_focussed != self.btn_player1.text_widget.color:
            self.btn_player1.text_widget.color = self.btn_player1.color_normal

        self.btn_player2.color_normal = pygame.Color(200, 50, 50) if self.btn_player1.text_widget.text == self.btn_player2.text_widget.text else self.btn_player2.text_widget.color_normal
        if self.btn_player2.color_normal != self.btn_player2.text_widget.color and self.btn_player2.color_focussed != self.btn_player2.text_widget.color:
            self.btn_player2.text_widget.color = self.btn_player2.color_normal

        self.gui.update(delta)        
        return self.next_gamestate

    def cleanup(self):
        pass

    def handle_event(self, event):
        self.gui.handle_event(event)

    # events
    def btn_ok_click(self, sender):
        self.next_gamestate = "main_menu"

    def _get_index_of_control_text(control_text):
        index = None
        for i, element in enumerate(Settings_menu.CONTROL_CHOICES):
            if element[0] == control_text:
                index = i
                break
        assert index is not None, "index not found"
        return index

    def toggle_control(self, btn, btn_number):
        current_text = btn.text_widget.text
        index = Settings_menu._get_index_of_control_text(current_text)
        new_index = index + 1
        if new_index >= len(Settings_menu.CONTROL_CHOICES):
            new_index = 0
        btn.text_widget.text = Settings_menu.CONTROL_CHOICES[new_index][0]
        Config.controls[btn_number - 1] = Settings_menu.CONTROL_CHOICES[new_index][1]

    def btn_control1_click(self, sender):
        self.toggle_control(sender, 1)

    def btn_control2_click(self, sender):
        self.toggle_control(sender, 2)

    def btn_score_limit_click(self, sender):
        current_score_limit = int(sender.text_widget.text)
        current_score_limit += 1
        if current_score_limit > Config.MAX_SCORE_LIMIT:
            current_score_limit = 1
        sender.text_widget.text = str(current_score_limit)
        Config.score_limit = current_score_limit
    