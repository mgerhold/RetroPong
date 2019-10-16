from gamestate import Gamestate
from racket import Racket
from control_keyboard import Control_keyboard
from control_mouse import Control_mouse
from control_ai import Control_ai
from ball import Ball
from text_widget import Text_widget
from gui_group import GUI_group
from config import Config
from globals import Globals
from sound_manager import Sound_manager
import pygame
import random

class Game(Gamestate):
    def __init__(self):
        super().__init__("game")
        self.next_gamestate = None
        self.rackets = [
            Racket(
                (Config.MARGIN, Config.SCREENHEIGHT // 2 - Config.RACKET_HEIGHT // 2),
                (Config.RACKET_WIDTH, Config.RACKET_HEIGHT)                
            ),
            Racket(
                (Config.SCREENWIDTH - Config.MARGIN - Config.RACKET_WIDTH, Config.SCREENHEIGHT // 2 - Config.RACKET_HEIGHT // 2),
                (Config.RACKET_WIDTH, Config.RACKET_HEIGHT)
            )
        ]
        self.ball = Ball(self.rackets, (Config.SCREENWIDTH // 2 - Config.BALL_SIZE // 2, Config.SCREENHEIGHT // 2 - Config.BALL_SIZE // 2))
        self.ball.on_boundary_hit.append(self.score_point)          # subscribe to event to update the score
        self.ball.on_boundary_hit.append(self.play_boundary_sound)  # play boundary sound
        self.ball.on_racket_hit.append(self.increase_speed)         # subscribe to event to increase speed on every racket hit
        self.ball.on_racket_hit.append(self.play_racket_sound)      # play racket bounce sound

        self.racket_controls = []
        for i, control in enumerate(Config.controls):            
            if control == "ai":
                self.racket_controls.append(Control_ai(self.rackets[i], self.ball))
                # nerf ai players - otherwise they are too strong
                self.rackets[i].max_speed = Config.AI_PLAYER_SPEED
            elif control == "mouse":
                self.racket_controls.append(Control_mouse(self.rackets[i]))
                self.rackets[i].max_speed = Config.MOUSE_SPEED # higher speed for mouse input
            elif control == "keyboard":
                self.racket_controls.append(Control_keyboard(self.rackets[i]))

        self.info_text = Text_widget(
            (Config.SCREENWIDTH // 2, Config.SCREENHEIGHT - Config.MARGIN),
            "ESC zum Beenden",
            color_normal=pygame.Color(100, 100, 100),
            text_justify="center",
            vertical_align="top"
        )

        self.score_widgets = [
            Text_widget((Config.MARGIN + Config.RACKET_WIDTH * 2, Config.MARGIN), "0"),
            Text_widget((Config.SCREENWIDTH - Config.MARGIN - Config.RACKET_WIDTH * 2, Config.MARGIN), "0", text_justify="right")
        ]

        self.countdown = Config.START_COUNTDOWN
        self.countdown_text = Text_widget(
            (Config.SCREENWIDTH // 2, Config.SCREENHEIGHT // 2),
            "",
            text_justify="center",
            vertical_align="center"
        )

        self.gui = GUI_group()
        self.gui.add(
            self.score_widgets[0],
            self.score_widgets[1],
            self.info_text,
            self.countdown_text
        )

        Sound_manager.change_song()

    def draw(self, surface):
        pygame.draw.line(surface, pygame.Color(180, 180, 180), (Config.SCREENWIDTH // 2, 0), (Config.SCREENWIDTH // 2, Config.SCREENHEIGHT - 1), Config.PLAYFIELD_LINE_WIDTH)
        for racket in self.rackets:
            racket.draw(surface)
        if self.countdown is None:
            self.ball.draw(surface)
        self.gui.draw(surface)

    def update(self, delta):
        # handle racket control (ai or keyboard or mouse)
        if self.countdown is None:
            for racket_control in self.racket_controls:
                racket_control.update(delta)
            
        # update rackets
        for racket in self.rackets:
            racket.update(delta)

        # update ball
        if self.countdown is None:
            self.ball.update(delta)

        # update countdown
        if self.countdown is not None:
            count_before = int(self.countdown + 1)
            self.countdown -= delta / 1000            
            count_after = int(self.countdown + 1)
            if count_before != count_after:
                if count_after >= 1:
                    Sound_manager.play("tick")
                else:
                    Sound_manager.play("start")
            self.countdown_text.text = f"Spielstart in {int(self.countdown + 1)} s..."
            if self.countdown <= 0:
                self.countdown = None
        else:
            self.countdown_text.text = ""

        # update gui
        self.gui.update(delta)

        return self.next_gamestate

    def handle_event(self, event):        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_gamestate = "main_menu"

    def play_boundary_sound(self, sender, boundary):
        if boundary == "top" or boundary == "bottom":
            Sound_manager.play("click")
        else:
            if self.get_winner() is None:
                Sound_manager.play("fail")

    def play_racket_sound(self, sender, racket):
        Sound_manager.play("racket")

    def get_winner(self):
        if int(self.score_widgets[0].text) >= Config.score_limit:
            return 1
        elif int(self.score_widgets[1].text) >= Config.score_limit:
            return 2
        else:
            return None

    def score_point(self, sender, boundary):        
        if boundary == "right":
            self.score_widgets[0].text = str(int(self.score_widgets[0].text) + 1)
            self.reset_game()
        elif boundary == "left":
            self.score_widgets[1].text = str(int(self.score_widgets[1].text) + 1)
            self.reset_game()
        winner = self.get_winner()
        if winner is not None:
            Globals.winner = winner
            self.next_gamestate = "gameover"

    def reset_game(self):
        self.ball.reset()
        for racket in self.rackets:
            racket.reset()
        self.countdown = Config.START_COUNTDOWN

    def increase_speed(self, sender, racket):
        vx = abs(self.ball.velocity[0]) + Config.SPEED_INCREASE + random.randint(0, Config.SPEED_RANDOMNESS + 1)
        vy = abs(self.ball.velocity[1]) + Config.SPEED_INCREASE + random.randint(- Config.SPEED_RANDOMNESS, Config.SPEED_RANDOMNESS + 1)
        if vx * self.ball.velocity[0] < 0:
            vx = -vx
        if vy * self.ball.velocity[1] < 0:
            vy = -vy
        self.ball.velocity = (vx, vy)
        

    def cleanup(self):
        pass