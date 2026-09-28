# 실습 과제 진행
from pico2d import*

import math
open_canvas(800,600)
character=load_image('character.png')

def draw_character(x,y):
    clear_canvas()
    character.draw(x,y)
    update_canvas()
    delay(0.01)

def move_circle():
    print('circle')
    for degree in range(360):
        theta=math.radians(degree)
        x=400+200*math.cos(theta)
        y=300+200*math.sin(theta)

        draw_character(x,y)

    pass

def move_top():
    print('top')
    for x in range(50, 751, 5):
        draw_character(x,550)
    pass

def move_right():
    print('right')
    for y in range(550, 51, -5):
        draw_character(750, y)
    pass

def move_bottom():
    print('bottom')
    for x in range(750, 51, -5):
        draw_character(x,50)
    pass

def move_left():
    print('left')
    for y in range(50, 551, 5):
        draw_character(50, y)
    pass

a=(100, 100)
b=(700,100)
c=(400,500)
n=60


def move_a_to_b():
    print('a to b')
    for step in range(n + 1):
        t = step / n

        x = a[0] + (b[0] - a[0]) * t
        y = a[1] + (b[1] - a[1]) * t

        draw_character(x, y)
    pass

def move_b_to_c():
    print('b to c')
    for step in range(n + 1):
        t = step / n

        x = b[0] + (c[0] - b[0]) * t
        y = b[1] + (c[1] - b[1]) * t

        draw_character(x, y)
    pass

def move_c_to_a():
    print('c to a')
    for step in range(n + 1):
        t = step / n

        x = c[0] + (a[0] - c[0]) * t
        y = c[1] + (a[1] - c[1]) * t

        draw_character(x, y)
    pass


def move_rectangle():
    print('rectangle')
    move_top()
    move_right()
    move_bottom()
    move_left()
    pass
def move_triangle():
    print('triangle')
    move_a_to_b()
    move_b_to_c()
    move_c_to_a()
    pass




while True:
    move_c_to_a()
    move_circle()
    move_rectangle()
    #move_triangle()
    pass


close_canvas()