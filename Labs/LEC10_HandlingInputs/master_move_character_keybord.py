from pico2d import *


SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 1024
CHARACTER_HALF_SIZE = 50
MOVE_SPEED = 300
FRAME_INTERVAL = 0.1


open_canvas(SCREEN_WIDTH, SCREEN_HEIGHT)
background = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')

running = True
x, y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
facing_right = True
pressed_keys = set()
frame = 0
animation_elapsed = 0.0
