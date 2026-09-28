from pico2d import *
import math

open_canvas(800, 600)
character = load_image('character.png')


def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(0.01)


def move_circle():
    center_x, center_y = 400, 300
    radius = 200
    for degree in range(360):
        theta = math.radians(degree)
        x = center_x + radius * math.cos(theta)
        y = center_y + radius * math.sin(theta)
        draw_character(x, y)
