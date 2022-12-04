from pico2d import *
import game_world

class Dash_effect:
    def __init__(self, x = 0, y = 0, dir = 1):
        self.image = load_image('image/animation_sheet.png')
        self.x, self.y, self.dir = x, y, dir

        self.timer = 10

    def draw(self):
        self.image.clip_draw(414 - self.dir * 46, 200, 92, 100, self.x, self.y) # dash_effect


    def update(self):
        self.timer -= 1
        if self.timer == 0:
            game_world.remove_object(self)