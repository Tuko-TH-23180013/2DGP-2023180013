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


def move_rectangle():
    for x in range(50, 751, 5):
        draw_character(x, 550)
    for y in range(550, 49, -5):
        draw_character(750, y)
    for x in range(750, 49, -5):
        draw_character(x, 50)
    for y in range(50, 551, 5):
        draw_character(50, y)
