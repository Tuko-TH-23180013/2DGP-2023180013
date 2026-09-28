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
    pass

def move_right():
    print('right')
    pass

def move_bottom():
    print('bottom')
    pass

def move_left():
    print('left')
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
    pass




while True:
    move_circle()
    move_rectangle()
    move_triangle()
    pass


close_canvas()