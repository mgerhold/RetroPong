import pygame
import random
from globals import Globals
from config import Config
from os import listdir
from os.path import isfile, join
import os

class Sound_manager:
    def play(sound):
        if sound in Sound_manager.sounds:
            Sound_manager.sounds[sound].play()
        else:
            print(f"Warning: Sound {sound} not found!")

    def change_song():
        if len(Sound_manager.songs) > 1:            
            pygame.mixer.music.set_endevent(Globals.SONG_END)
            pygame.mixer.music.set_volume(Config.MAIN_VOLUME)
            old_song = Sound_manager.current_song
            new_song = None
            while new_song is None or old_song == new_song:
                new_song = random.choice(Sound_manager.songs)
            pygame.mixer.music.load(new_song)
            pygame.mixer.music.play()

    def stop_music():
        pygame.mixer.music.set_endevent(0)
        pygame.mixer.music.stop()

Sound_manager.sounds = {
    "menu_move" : pygame.mixer.Sound("sfx/menu_move.wav"),
    "menu_select" : pygame.mixer.Sound("sfx/menu_select.wav"),
    "click" : pygame.mixer.Sound("sfx/click.wav"),
    "racket" : pygame.mixer.Sound("sfx/racket.wav"),
    "fail" : pygame.mixer.Sound("sfx/fail.wav"),
    "gameover" : pygame.mixer.Sound("sfx/gameover.wav"),
    "tick" : pygame.mixer.Sound("sfx/tick.wav"),
    "start" : pygame.mixer.Sound("sfx/start.wav")
}
for key, sound in Sound_manager.sounds.items():
    sound.set_volume(Config.MAIN_VOLUME)

Sound_manager.songs = []
for file in listdir("music/"):
    if file.endswith(".ogg"):
        Sound_manager.songs.append(join("music/", file))
Sound_manager.current_song = None