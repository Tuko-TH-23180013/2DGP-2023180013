# 실습 과제 진행
from pico2d import*

open_canvas(800,600)
def move_circle():
    print('circle')
    
    character=load_image('character.png')

    clear_canvas()
    character.draw(400,300)
    update_canvas()
    delay(1)


    pass
def move_rectangle():
    print('rectangle')
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