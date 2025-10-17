from pico2d import *
from grass import Grass
from boy import Boy

def reset_world():
    global world
    world = []
    grass = Grass()
    world.append(grass)
    boy= Boy()
    world.append(boy)

    pass

def handle_events():
    pass

def update_world():
    for o in world:
        o.update()
    pass

def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()
    pass

running=True

open_canvas()
reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)
close_canvas()
