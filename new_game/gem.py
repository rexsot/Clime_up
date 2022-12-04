from pico2d import *
import game_world
import server

class Gem_full:
    def __init__(self, x = 0, y = 0):
        self.image = load_image('image/gem_full.png')
        self.sound_return = load_wav('sound/gem_return.wav')
        self.sound_return.set_volume(32)

        self.x, self.y = x, y

    def draw(self):
        self.image.draw(self.x, self.y)
        #draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def handle_collision(self, other, group):
        game_world.remove_object(self) # 자신을 지우고
        gem_empty = Gem_empty(self.x, self.y) # 현 위치에
        game_world.add_object(gem_empty, 1) # gem_empty 생성
        gem_empty.sound_touch.play(1)  # 젬 소멸 소리 출력


    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30

class Gem_empty:
    def __init__(self, x = 0, y = 0):
        self.image = load_image('image/gem_empty.png')
        self.sound_touch = load_wav('sound/gem_touch.wav')
        self.sound_touch.set_volume(32)

        self.x, self.y = x, y
        self.timer = 180

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        self.timer -= 1
        if self.timer == 0:
            game_world.remove_object(self)  # 자신을 지우고
            gem_full = Gem_full(self.x, self.y)  # 현 위치에
            game_world.add_object(gem_full, 1)  # gem_full 생성
            game_world.add_collision_pairs(server.player, gem_full, 'player:gem_full')
            gem_full.sound_return.play(1)  # 젬 생성 소리 출력


