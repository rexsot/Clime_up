from pico2d import *
import game_world

class Strawberry_red:
    def __init__(self, x = 0, y = 0):
        self.image = load_image('image/strawberry_red.png') # 빨강 딸기
        self.x, self.y = x, y

    def draw(self):
        self.image.draw(self.x, self.y)
        #draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x - 30 , self.y - 40, self.x + 30 , self.y + 40

    def handle_collision(self, other, group):
        if 'player:straw_red' == group: # 플레이어와 충돌시
            game_world.remove_object(self)  # 자신을 지우고
            score = Score(self.x, self.y)  # 현 위치에
            game_world.add_object(score, 1)  # 스코어 생성
            score.sound.play(1)  # 딸기 획득 소리 출력

class Strawberry_gold:
    def __init__(self, x = 0, y = 0):
        self.image = load_image('image/strawberry_gold.png') # 빨강 딸기
        self.x, self.y = x, y

    def draw(self):
        self.image.draw(self.x, self.y)
        #draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x - 30 , self.y - 40, self.x + 30 , self.y + 40

    def handle_collision(self, other, group):
        if 'player:straw_gold' == group: # 플레이어와 충돌시
            game_world.remove_object(self)  # 자신을 지우고
            score_10000 = Score_10000(self.x, self.y)  # 현 위치에
            game_world.add_object(score_10000, 1)  # 스코어 생성
            score_10000.sound.play(1)  # 딸기 획득 소리 출력

class Score:
    def __init__(self, x = 0, y = 0):
        self.image = load_image('image/score.png')
        self.sound = load_wav('sound/strawberry_get.wav') # 딸기 먹는 소리

        self.sound.set_volume(32)

        self.x, self.y = x, y
        self.timer = 150

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        self.timer -= 1
        self.y += 0.3  # 조금씩 위로 올라간다.
        if self.timer == 0:
            game_world.remove_object(self)  # 자신을 지운다.

class Score_10000:
    def __init__(self, x = 0, y = 0):
        self.image = load_image('image/score.png')
        self.sound = load_wav('sound/stage_clear.wav') # 황금 딸기 먹는 소리

        self.sound.set_volume(32)

        self.x, self.y = x, y
        self.timer = 180

    def draw(self):
        self.image.draw(self.x+12, self.y)
        self.image.draw(self.x-12, self.y)

    def update(self):
        self.timer -= 1
        self.y += 0.2  # 조금씩 위로 올라간다.
        if self.timer == 0:
            game_world.remove_object(self)  # 자신을 지운다.



#self.image_gold = load_image('image/ptrawberry_gold.png')  # 황금 딸기