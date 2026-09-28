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


def move_between(start, end, steps=60):
    for step in range(steps + 1):
        t = step / steps
        x = start[0] + (end[0] - start[0]) * t
        y = start[1] + (end[1] - start[1]) * t
        draw_character(x, y)


def move_triangle():
    a = (100, 100)
    b = (700, 100)
    c = (400, 500)
    move_between(a, b)
    move_between(b, c)
    move_between(c, a)

try:
    while True:
        move_circle()
        move_rectangle()
        move_triangle()
finally:
    close_canvas()
