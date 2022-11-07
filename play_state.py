from pico2d import *
import game_framework

frame_time = 0.013
press_space = 0
jump_time = 0
dash_time = 0


class Player:
    def __init__(self):
        self.loc_x, self.loc_y = 200, 150 # 위치
        self.vel_x, self.vel_y = 0, 0 # 속도
        self.acc_x, self.acc_y = 0, 0 # 가속도
        self.dir_x, self.dir_y = 0, 0  # 방향키의 방향

        self.face_dir = 1 # 보고 있는 방향 - 좌 = -1, 우 = 1
        self.grounded = 0 # 0일때 접지, 1일때 체공
        self.frame = 0 # 프레임 수

        self.image = load_image('animation_sheet.png')

    def update(self):
        self.frame = (self.frame + 1) % 20 # 프레임 계산

        # X 계산

        # if (0 < self.loc_x + self.dir_x * 9 and self.loc_x + self.dir_x * 9 < X_MAX): # x좌표 제한
        #     self.loc_x += self.dir_x * 9 # x축 이동

        # 속도의 방향(vel_x)과 키의 방향(dir_x)이 일치할 때 덜 감속하고, 불일치할 때(방향키가 중립일 때 포함) 더 감속한다.
        # 9 곱해야함

        if self.vel_x < 810: # 속도 90미만
            if self.dir_x == 1: # 현재 이동방향으로 키입력
                self.acc_x = 97.47
            else: # 반대방향/중립
                if 0 < self.vel_x:
                    self.acc_x = -97.47
        elif 810 < self.vel_x : # 속도 90이상
            if self.grounded == 0: # 접지
                if self.dir_x == 1: # 현재 이동방향으로 키입력
                    self.acc_x = -59.94
                else: # 반대방향/중립
                    self.acc_x = -150.03
            else: # 체공
                if self.dir_x == 1: # 현재 이동방향으로 키입력
                    self.acc_x = -38.97
                else: # 반대방향/중립
                    self.acc_x = -97.47

        self.loc_x += self.vel_x * frame_time  # 프레임당 속도(player.update가 초당 프레임 수만큼 실행되므로, 역산해서 더한다.)
        self.vel_x += self.acc_x  # 프레임당 가속도


        # 90 x 60 = 540
#dir_x가 입력된 방향, face_dir은 마지막으로 입력된 dir_x, vel_x가 x축 속력

        if self.dir_x > 0: # 방향 판별 - vel_x로 변경해야함
            self.face_dir = 1
        if self.dir_x < 0:
            self.face_dir = -1




        # Y 계산
        global press_space
        global jump_time

        if self.vel_y > 945: # 상승 종단속도
            self.vel_y = 945

        if self.vel_y < -1440: # 하강 종단속도
            self.vel_y = -1440

        self.loc_y += self.vel_y * frame_time # 프레임당 속도(player.update가 초당 프레임 수만큼 실행되므로, 역산해서 더한다.)
        self.vel_y += self.acc_y # 프레임당 가속도

        if self.loc_y > 150: # 체공판별(임시)
            self.grounded = 1
        elif self.loc_y < 150: # 접지
            self.loc_y = 150
            self.vel_y = 0
            self.acc_y = 0
            self.grounded = 0

        if jump_time < 12 and press_space == 1: #점프 직후 점프키 홀딩시, 12프레임까지 가속도 감소 없음
            jump_time += 1
            #print(jump_time)
            self.acc_y = 0

        elif self.grounded == 1: #체공시
            if -405 < self.vel_y < 405 and press_space == 1: # 최고점 근처에서 점프키 홀딩(감속 하강)
                self.acc_y = -67.5 #중력 반감
            else:
                self.acc_y = -135 # 기본중력



    def draw(self): # 캐릭터 모션 출력
        if self.grounded == 0:  # 접지시
            if self.dir_x == 0:  # 접지-정지
                self.image.clip_draw(46 - self.face_dir * 46, 200, 92, 100, self.loc_x, self.loc_y)
            else:  # 접지-이동
                self.image.clip_draw(self.frame * 92, 50 + self.face_dir * 50, 92, 100, self.loc_x, self.loc_y)
        else:  # 체공
            self.image.clip_draw(240 - self.face_dir * 46, 200, 92, 100, self.loc_x, self.loc_y)


def handle_events():
    global running
    global press_space
    global jump_time

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT: # 창닫기
            game_framework.quit()

        elif event.type == SDL_KEYDOWN: # 키 누를때
            if event.key == SDLK_ESCAPE: # esc
                game_framework.quit() #game_framework.change_state(logo_state)
            #if event.key == SDLK_x:  # x(대시)
            if event.key == SDLK_RIGHT: # 우
                player.dir_x += 1
            if event.key == SDLK_LEFT:  # 좌
                player.dir_x -= 1
            if event.key == SDLK_SPACE: # 스페이스 바 입력
                press_space = 1
                if player.grounded == 0:  #접지중 점프시
                    jump_time = 0
                    player.acc_y = 945
                    #player.vel_x += player.dir_x * 360 # 이동하며 점프시 40(360)의 가속을 받는다.

        elif event.type == SDL_KEYUP: #키 땔때
            if event.key == SDLK_RIGHT:
                player.dir_x -= 1
            elif event.key == SDLK_LEFT:
                player.dir_x += 1
            if event.key == SDLK_SPACE: # 스페이스바가 때질 때
                press_space = 0


X_MAX = 1920
Y_MAX = 1080

player = None
running = True

def enter():
    global player, running
    player = Player()
    running = True

def exit():
    global player
    del player

def update():
    player.update()
    delay(frame_time)
    pass

def draw():
    clear_canvas()
    player.draw()
    update_canvas()
    pass

def pause():
    pass

def resume():
    pass