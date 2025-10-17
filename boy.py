from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT
from state_machine import StateMachine

def right_down(e):
    return e[0]=='INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def right_up(e):
    return e[0]=='INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_down(e):
    return e[0]=='INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def left_up(e):
    return e[0]=='INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT
def a_down(e): return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a
def time_out(e): return e[0] == 'TIME_OUT'
from pico2d import *

class AUTORUN:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        self.boy.start_time = get_time()
        self.boy.speed = 10
        if self.boy.face_dir == 0:
            self.boy.face_dir = 1
        self.boy.dir = self.boy.face_dir

    def exit(self, e):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8
        self.boy.x += self.boy.dir * self.boy.speed

        if self.boy.x > 800:
            self.boy.x = 800
            self.boy.dir = -1
            self.boy.face_dir = -1
        elif self.boy.x < 0:
            self.boy.x = 0
            self.boy.dir = 1
            self.boy.face_dir = 1

        if get_time() - self.boy.start_time > 5:
            self.boy.state_machine.handle_state_event(('TIME_OUT', None))

    def draw(self):
        if self.boy.face_dir == 1:
            self.boy.image.clip_draw(self.boy.frame * 100, 100, 100, 100, self.boy.x, self.boy.y, 120, 120)
        else:
            self.boy.image.clip_draw(self.boy.frame * 100, 0, 100, 100, self.boy.x, self.boy.y, 120, 120)

class RUN:

    def __init__(self, boy):
        self.boy = boy

    def enter(self,e):
        if right_down(e) or left_up(e):
            self.boy.dir = self.boy.face_dir = 1
        elif left_down(e) or right_up(e):
            self.boy.dir = self.boy.face_dir = -1

    def exit(self,e):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8

        self.boy.x += self.boy.dir * 5

    def draw(self):
        if self.boy.face_dir == 1: # right
            self.boy.image.clip_draw(self.boy.frame * 100, 100, 100, 100, self.boy.x, self.boy.y)
        else: # face_dir == -1: # left
            self.boy.image.clip_draw(self.boy.frame * 100, 0, 100, 100, self.boy.x, self.boy.y)

class Idle:

    def __init__(self, boy):
        self.boy = boy

    def enter(self,e):
        self.boy.dir = 0
        self.boy.wait_start_time = get_time()
    def exit(self,e):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8
        if get_time() - self.boy.wait_start_time > 2.0:
            self.boy.state_machine.handle_state_event(('TIME_OUT', None))

    def draw(self):
        if self.boy.face_dir == 1: # right
            self.boy.image.clip_draw(self.boy.frame * 100, 300, 100, 100, self.boy.x, self.boy.y)
        else: # face_dir == -1: # left
            self.boy.image.clip_draw(self.boy.frame * 100, 200, 100, 100, self.boy.x, self.boy.y)

class Boy:
    def __init__(self):
        self.image = load_image('animation_sheet.png')
        self.x, self.y = 100, 90
        self.frame = 0
        self.dir = 0
        self.face_dir = 1
        self.IDLE = Idle(self)
        self.RUN = RUN(self)
        self.AUTORUN = AUTORUN(self)
        self.state_machine= (StateMachine(
            self.IDLE,
            {
                self.IDLE: { right_down: self.RUN, left_down: self.RUN, right_up: self.RUN,
                            left_up: self.RUN,a_down:self.AUTORUN},
                self.RUN: {right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE, left_down: self.IDLE},
                self.AUTORUN: {time_out: self.IDLE}
            }))
    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
    pass

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))
        pass
