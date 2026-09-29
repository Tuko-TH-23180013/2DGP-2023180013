import json

from pico2d import *


SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
FRAME_DELAY = 0.09


open_canvas(SCREEN_WIDTH, SCREEN_HEIGHT)
background = load_image('fantasy_forest_background.png')
running = True

while running:
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

    background.draw(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                    SCREEN_WIDTH, SCREEN_HEIGHT)
    update_canvas()
    delay(FRAME_DELAY)

close_canvas()
