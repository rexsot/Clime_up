from pico2d import *

class Spike:
    def __init__(self, x = 0, y = 0, dir = 1): # 1 - 상, 2 - 하, 3 - 좌, 4 - 우
        self.image_up = load_image('image/spike_up.png')  # 상
        self.image_down = load_image('image/spike_down.png') # 하
        self.image_left = load_image('image/spike_left.png')  # 좌
        self.image_right = load_image('image/spike_right.png') # 우

        self.x, self.y, self.dir = x, y, dir

    def draw(self):
        if self.dir == 1:
            self.image_up.draw(self.x, self.y)
        elif self.dir == 2:
            self.image_down.draw(self.x, self.y)
        elif self.dir == 3:
            self.image_left.draw(self.x, self.y)
        else:
            self.image_right.draw(self.x, self.y)
        #draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        if self.dir == 1 or self.dir == 2:
            return self.x - 30 , self.y - 24, self.x + 30 , self.y + 24

        return self.x - 24 , self.y - 30, self.x + 24 , self.y + 30

    def handle_collision(self, other, group):
        pass