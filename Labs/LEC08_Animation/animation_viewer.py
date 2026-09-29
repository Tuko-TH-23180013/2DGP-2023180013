import json

from pico2d import *


SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
FRAME_DELAY = 0.09


open_canvas(SCREEN_WIDTH, SCREEN_HEIGHT)
background = load_image('fantasy_forest_background.png')
knight_atlas = load_image('fantasy_knight_variable_atlas.png')
with open('fantasy_knight_frames.json', encoding='utf-8') as metadata_file:
    atlas_metadata = json.load(metadata_file)
action_metadata = atlas_metadata['actions']
ANIMATION_SEQUENCE = ('idle', 'walk', 'run', 'jump', 'attack')
sequence_index = 0
action = ANIMATION_SEQUENCE[sequence_index]
frame = 0
running = True

while running:
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

    background.draw(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                    SCREEN_WIDTH, SCREEN_HEIGHT)
    animation = action_metadata[action]
    action_frame_count = animation['frame_count']
    sprite_frame = animation['frames'][frame]
    update_canvas()
    delay(FRAME_DELAY)

close_canvas()
