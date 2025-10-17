from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT

class Boy:
    def __init__(self):
        self.image = load_image('animation_sheet.png')
        self.x, self.y = 100, 90
        self.frame = 0
        self.dir = 0
        self.face_dir = 1

    def update(self):
        self.frame = (self.frame + 1) % 8

    def draw(self):
        if self.face_dir == 1:
            self.image.clip_draw(self.frame * 100, 100, 100, 100, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)
    pass
