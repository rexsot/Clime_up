from pico2d import *
import game_framework

frame_time = 0.013
#dash_time = 0

def sig(a, b): # 두 수의 부호 같다면 1리턴, 아니라면 -1 리턴
    if a > 0 and b >= 0:
        return 1
    if a < 0 and b <= 0:
        return 1
    return -1

def vec(a): # 양수면 1, 음수면 -1, 0은 0리턴
    if a > 0:
        return 1
    if a < 0:
        return -1
    return 0

class Player:
    def __init__(self):
        self.loc_x, self.loc_y = 200, 150 # x,y 위치
        self.vel_x, self.vel_y = 0, 0 # x,y 속도
        self.acc_x, self.acc_y = 0, 0 # x,y 가속도
        self.dir_x, self.dir_y = 0, 0  # x,y 방향키의 방향
        self.press_space, self.jump_time = 0, 0 # 스페이스 바 눌림, 점프 시간

        self.face_dir = 1 # 보고 있는 방향(좌 = -1, 우 = 1)
        self.midair = 0 # 접지 = 0, 체공 = 1
        self.frame = 0 # 현재 프레임 수

        self.image = load_image('image/animation_sheet.png') # 이미지

    def update(self):
        self.frame = (self.frame + 1) % 20 # 프레임 계산

        # 보는 방향 판별
        if self.dir_x > 0:
            self.face_dir = 1
        if self.dir_x < 0:
            self.face_dir = -1

        # if (0 < self.loc_x + self.dir_x * 9 and self.loc_x + self.dir_x * 9 < X_MAX): # x좌표 제한
        #     self.loc_x += self.dir_x * 9 # x축 이동


        # X 계산

        # 속도의 방향(vel_x)과 키의 방향(dir_x)이 일치할 때 덜 감속하고, 불일치할 때(방향키가 중립일 때 포함) 더 감속한다.
        s = sig(self.dir_x, self.vel_x) # 방향과 속도가 같다면 1, 아니면 -1
        vel_x_abs = abs(self.vel_x) # x 속도의 절댓값(속력)

        if self.dir_x == 0: # 방향키가 중립일 때
            if vel_x_abs <= 97.5: # 최소 속력이하 - 정지
                self.vel_x = 0 # 속도 0
                self.acc_x = 0 # 가속도 0

            else: # 최소 속력 초과 - 감속
                if 810 < vel_x_abs and self.midair == 0: # 속력 810 이상 AND 접지중일 때(마찰감속)
                    self.acc_x = vec(self.vel_x) * -150 # 가속도 추가 감속
                    
                else: # 속력 810 미만 OR 체공중일 때
                    self.acc_x = vec(self.vel_x) * -97.5 # 가속도 감속

        else: # 방향키 비중립
            if vel_x_abs < 810: # 속력 810 미만
                self.acc_x = self.dir_x * 97.5 # 가속도 가속
                
            else: # 속력 810 이상
                if self.midair == 0: # 접지
                    self.acc_x = vec(self.vel_x) * -(135 - s * 45)  # 이동방향이 같다면 -60, 다르다면 -150
                    
                else:  # 체공
                    self.acc_x = vec(self.vel_x) * -(68.75 - s * 28.75)  # 이동방향이 같다면 -40, 다르다면 -97.5

                #self.acc_x = vec(self.vel_x) * 97.5 * -s # 이동방향이 같다면 감속, 아니라면 가속
                #self.acc_x = self.dir_x * -97.5 * s # 추가 감속

        self.loc_x += self.vel_x * frame_time  # 프레임당 속도(player.update가 초당 프레임 수만큼 실행되므로, 역산해서 더한다.)
        self.vel_x += self.acc_x  # 프레임당 가속도

        # Y 계산

        if self.vel_y > 945: # 상승 종단속도
            self.vel_y = 945

        if self.vel_y < -1440: # 하강 종단속도
            self.vel_y = -1440

        self.loc_y += self.vel_y * frame_time # 프레임당 속도(player.update가 초당 프레임 수만큼 실행되므로, 역산해서 더한다.)
        self.vel_y += self.acc_y # 프레임당 가속도

        if self.loc_y > 150: # 체공판별(임시)
            self.midair = 1

        elif self.loc_y < 150: # 접지시
            self.loc_y = 150
            self.vel_y = 0
            self.acc_y = 0
            self.midair = 0

        if self.jump_time < 12 and self.press_space == 1: #점프 직후 점프키 홀딩시, 12프레임까지 가속도 감소 없음
            self.jump_time += 1
            #print(jump_time)
            self.acc_y = 0

        elif self.midair == 1: #체공시
            if -405 < self.vel_y < 405 and self.press_space == 1: # 최고점 근처에서 점프키 홀딩(감속 하강)
                self.acc_y = -67.5 #중력 반감
            else:
                self.acc_y = -135 # 기본중력

        # if (abs(self.acc_y)) > 0:
        #     print(self.acc_y)

    def draw(self): # 캐릭터 모션 출력
        if self.midair == 0:  # 접지시
            if self.dir_x == 0:  # 접지-정지
                self.image.clip_draw(46 - self.face_dir * 46, 200, 92, 100, self.loc_x, self.loc_y)
            else:  # 접지-이동
                self.image.clip_draw(self.frame * 92, 50 + self.face_dir * 50, 92, 100, self.loc_x, self.loc_y)
        else:  # 체공
            self.image.clip_draw(240 - self.face_dir * 46, 200, 92, 100, self.loc_x, self.loc_y)


def handle_events():

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
                player.press_space = 1
                if player.midair == 0:  #접지중 점프시
                    player.jump_time = 0
                    player.acc_y = 945
                    #player.vel_x += player.dir_x * 360 # 이동하며 점프시 40(360)의 가속을 받는다.

        elif event.type == SDL_KEYUP: #키 땔때
            if event.key == SDLK_RIGHT:
                player.dir_x -= 1
            elif event.key == SDLK_LEFT:
                player.dir_x += 1
            if event.key == SDLK_SPACE: # 스페이스바가 때질 때
                player.press_space = 0
                player.jump_time = 30

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