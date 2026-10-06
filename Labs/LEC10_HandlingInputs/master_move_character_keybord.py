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
previous_time = get_time()


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key in (SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN):
                pressed_keys.add(event.key)
        elif event.type == SDL_KEYUP:
            pressed_keys.discard(event.key)


def update_character(delta_time):
    global x, y, facing_right, frame, animation_elapsed

    dx = int(SDLK_RIGHT in pressed_keys) - int(SDLK_LEFT in pressed_keys)
