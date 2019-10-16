import json
import os

class Config:
    SCREENWIDTH = 800
    SCREENHEIGHT = 600
    MAIN_VOLUME = 0.8
    MAX_FPS = 120
    MARGIN = 20
    START_COUNTDOWN = 3
    RACKET_WIDTH = 15
    RACKET_HEIGHT = 80
    RACKET_SPEED = 500
    MOUSE_SPEED = 2000 # basically unlimited
    AI_PLAYER_SPEED = 320
    BALL_START_VELOCITY = (350, -160)
    BALL_SIZE = 10
    SPEED_INCREASE = 10
    SPEED_RANDOMNESS = 10
    controls = [
        "keyboard",
        "ai"
    ]
    MAX_SCORE_LIMIT = 10
    score_limit = 3
    PLAYFIELD_LINE_WIDTH = 5

    def _save():
        config = {k : v for k, v in vars(Config).items() if not k.startswith("_")}
        with open("config.json", "w") as fp:
            json.dump(config, fp)

    def _load():
        if os.path.isfile("config.json"):
            with open("config.json") as fp:
                config = json.load(fp)
                for key, value in config.items():
                    setattr(Config, key, value)