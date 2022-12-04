from pico2d import *

col_left, col_down, col_right, col_up = 0, 0, 0, 0

class Plat_iron:
    def __init__(self, x = 0, y = 0, dir = -1): # dir = -1일때 가로, dir = 1일때 세로
        self.image_row = load_image('image/plat_iron_row.png') # 가로
        self.image_col = load_image('image/plat_iron_col.png') # 세로
        self.x, self.y, self.dir = x, y, dir

    def draw(self):
        if self.dir == -1:
            self.image_row.draw(self.x, self.y)
        else:
            self.image_col.draw(self.x, self.y)
        #draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x - (75 - self.dir * 45) , self.y - (75 + self.dir * 45), \
               self.x + (75 - self.dir * 45) , self.y + (75 + self.dir * 45)

        #self.x - 120, self.y - 30, self.x + 120, self.y + 30 # 가로 , -1
        #self.x - 30, self.y - 120, self.x + 30, self.y + 120 # 세로, 1

    def handle_collision(self, other, group):
        global col_left, col_down, col_right, col_up
        if 'player:plat_iron' == group: # 플레이어와 충돌시
            col_left, col_down, col_right, col_up = self.get_bb()