import json

from pico2d import *


SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
FRAME_DELAY = 0.09
CHARACTER_SCALE = 3.7


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
    source_left = sprite_frame['x']
    source_bottom = (atlas_metadata['atlas_height']
                     - sprite_frame['y'] - sprite_frame['height'])
    source_width = sprite_frame['width']
    source_height = sprite_frame['height']
    local_center_x = (sprite_frame['source_left'] + source_width / 2
                      - atlas_metadata['source_cell_width'] / 2)
    local_center_y = (atlas_metadata['source_cell_height'] / 2
                      - sprite_frame['source_top'] - source_height / 2)
    draw_x = SCREEN_WIDTH // 2 + int(local_center_x)
    draw_y = SCREEN_HEIGHT // 2 + int(local_center_y * CHARACTER_SCALE)
    draw_width = int(source_width * CHARACTER_SCALE)
    draw_height = int(source_height * CHARACTER_SCALE)
    draw_x = SCREEN_WIDTH // 2 + int(local_center_x * CHARACTER_SCALE)
    knight_atlas.clip_draw(
        source_left, source_bottom, source_width, source_height,
        draw_x, draw_y, draw_width, draw_height,
    )
    update_canvas()
    frame += 1
    if frame >= action_frame_count:
        frame = 0
    delay(FRAME_DELAY)

close_canvas()
