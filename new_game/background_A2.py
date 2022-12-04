from pico2d import *
import game_framework

class Background_A2:
    def __init__(self):
        self.image = load_image('image/background_2.png')
        self.bgm = load_music('sound/Z_A2.mp3')
        self.bgm.set_volume(32)
        self.bgm.repeat_play()

        self.size_x = game_framework.X_MAX
        self.size_y = game_framework.Y_MAX
        self.x = game_framework.X_MAX/2
        self.y = game_framework.Y_MAX/2


    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, self.size_x, self.size_y, self.x, self.y)
