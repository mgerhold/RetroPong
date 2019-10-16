from globals import Globals
from config import Config
from gamestate_manager import Gamestate_manager
import os
import pygame

if __name__ == "__main__":
    # load config
    Config._load()

    # initialize pygame
    os.environ['SDL_VIDEO_CENTERED'] = '1' # open pygame window centered on the screen
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    from sound_manager import Sound_manager # import has to happen after pygame.init() ! ! !
    pygame.font.init()    
    Globals.font = pygame.font.Font("PressStart2P.ttf", 17)
    screen = pygame.display.set_mode((Config.SCREENWIDTH, Config.SCREENHEIGHT))
    clock = pygame.time.Clock()

    # initialize gamestate manager and load main menu
    gamestate_manager = Gamestate_manager()
    gamestate_manager.change_gamestate('main_menu')        

    # game loop
    running = True
    while running:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == Globals.SONG_END:
                Sound_manager.change_song()
            else:
                gamestate_manager.handle_event(event)

        # update game logic and check if game should continue running
        if clock.get_time() <= 100: # pause game while window is getting dragged
            running = running and gamestate_manager.update(clock.get_time())

        # draw
        screen.fill(pygame.Color("black"))
        gamestate_manager.draw(screen)
        pygame.display.flip()

        # show fps in title bar and limit fps
        pygame.display.set_caption(f"RETRO-PONG - {round(clock.get_fps())} fps")
        clock.tick(Config.MAX_FPS)

    Config._save()