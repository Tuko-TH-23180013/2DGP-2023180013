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

#대각선 이동 구현
ex1=(100, 100)
ex2=(700,100)

n=12
#n은 이동 간격, 예시로 12 잡음
for step in range(n + 1):
    t = step / n
    x1=100+(700-100)*t
y1=100+(100-100)*t
#t=0이면 시작점
#t=1이면 끝점



def move_a_to_b():
    print('a to b')
    pass

def move_b_to_c():
    print('b to c')
    pass

def move_c_to_a():
    print('c to a')
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
    move_circle()
    move_rectangle()
    move_triangle()
    pass


close_canvas()