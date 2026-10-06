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
    dy = int(SDLK_UP in pressed_keys) - int(SDLK_DOWN in pressed_keys)
    moving = dx != 0 or dy != 0

    if dx > 0:
        facing_right = True
    elif dx < 0:
        facing_right = False

    if moving:
        distance = MOVE_SPEED * delta_time
        if dx and dy:
            distance *= 0.70710678
        x += dx * distance
        y += dy * distance
        x = max(CHARACTER_HALF_SIZE, min(SCREEN_WIDTH - CHARACTER_HALF_SIZE, x))
        y = max(CHARACTER_HALF_SIZE, min(SCREEN_HEIGHT - CHARACTER_HALF_SIZE, y))

    animation_elapsed += delta_time
    while animation_elapsed >= FRAME_INTERVAL:
        frame = (frame + 1) % 8
        animation_elapsed -= FRAME_INTERVAL

    return moving


def draw_character(moving):
    if moving:
        row = 1 if facing_right else 0
    else:
        row = 3 if facing_right else 2
    character.clip_draw(frame * 100, row * 100, 100, 100, int(x), int(y))


while running:
    now = get_time()
    delta_time = min(now - previous_time, 0.05)
    previous_time = now

    handle_events()
    moving = update_character(delta_time)

