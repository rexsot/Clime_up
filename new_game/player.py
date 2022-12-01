import game_framework
from pico2d import *

frame_time = 0.014

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

# 1. 이벤트 정의 - KD = KEY_DOWN, KU = KEY_UP

RIGHT_KD, LEFT_KD, UP_KD, DOWN_KD, X_KD, SPACE_KD,\
RIGHT_KU, LEFT_KU, UP_KU, DOWN_KU, SPACE_KU, ENTER_DASH, DASH_TIMER = range(13)

# DASH_TIMER, COLL_TIMER, DIE_TIMER - 대시 시간, 대시 충돌 시간, 사망시간
# DASH_TIMER: DASH_STATE -> MOVE_STATE
# COLL_TIMER: DASH_STATE -> DASH_COLL_STATE
# DIE_TIMER: MOVE_STATE/DASH_STATE -> DIE_STATE

key_event_table = {
    # 방향키 누르기
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_KD,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_KD,
    (SDL_KEYDOWN, SDLK_UP): UP_KD,
    (SDL_KEYDOWN, SDLK_DOWN): DOWN_KD,

    # x, 스페이스바 누르기
    (SDL_KEYDOWN, SDLK_x): X_KD,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE_KD,

    # 방향키, 스페이스바 때기
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_KU,
    (SDL_KEYUP, SDLK_LEFT): LEFT_KU,
    (SDL_KEYUP, SDLK_UP): UP_KU,
    (SDL_KEYUP, SDLK_DOWN): DOWN_KU,
    (SDL_KEYUP, SDLK_SPACE): SPACE_KU
}

class MOVE_STATE:

    def enter(player, event):
        if event == RIGHT_KD: # 우 입력
            player.dir_x += 1
        elif event == RIGHT_KU: # 우 해제
            player.dir_x -= 1

        if event == LEFT_KD: # 좌 입력
            player.dir_x -= 1
        elif event == LEFT_KU: # 좌 해제
            player.dir_x += 1

        if event == UP_KD: # 상 입력
            player.dir_y += 1
        elif event == UP_KU: # 상 해제
            player.dir_y -= 1

        if event == DOWN_KD: # 하 입력
            player.dir_y -= 1
        elif event == DOWN_KU: # 하 해제
            player.dir_y += 1

        if event == SPACE_KD: # 점프 입력
            player.press_space = 1
            if player.midair == 0:  # 접지중 점프시
                player.jump_time = 0
                player.acc_y = 945
                player.vel_x += player.dir_x * 360  # 이동하며 점프시 40(360)의 가속을 받는다.

        elif event == SPACE_KU: # 점프 해제
            player.press_space = 0
            player.jump_time = 30

        if player.dash_count > 0: # 대시 가능할 때
            if event == X_KD: # 대시 입력
                player.dash.count -= 1
                player.add_event(ENTER_DASH)

    def exit(player, event):
        pass

    def do(player):
        player.frame = (player.frame + 1) % 20  # 프레임 계산

        # 보는 방향 판별
        if player.dir_x > 0:
            player.face_dir = 1
        if player.dir_x < 0:
            player.face_dir = -1

        # x좌표 제한
        # if (0 < player.loc_x + player.dir_x * 9 and player.loc_x + player.dir_x * 9 < X_MAX):

        # ===== X 계산 =====

        # 속도의 방향(vel_x)과 키의 방향(dir_x)이 일치할 때 덜 감속하고, 불일치할 때(방향키가 중립일 때 포함) 더 감속한다.

        s = sig(player.dir_x, player.vel_x)  # 방향과 속도가 같다면 1, 아니면 -1
        vel_x_abs = abs(player.vel_x)  # x 속도의 절댓값(속력)

        if player.dir_x == 0:  # 방향키가 중립일 때
            if vel_x_abs <= 97.5:  # 최소 속력 이하 - 정지
                player.vel_x = 0  # 속도 0
                player.acc_x = 0  # 가속도 0

            else:  # 최소 속력 초과 - 감속
                if 810 < vel_x_abs and player.midair == 0:  # 속력 810 이상 AND 접지중일 때(마찰감속)
                    player.acc_x = vec(player.vel_x) * -150  # 가속도 추가 감속

                else:  # 속력 810 미만 OR 체공중일 때
                    player.acc_x = vec(player.vel_x) * -97.5  # 가속도 감속

        else:  # 방향키 비중립
            if vel_x_abs < 810:  # 속력 810 미만
                player.acc_x = player.dir_x * 97.5  # 가속도 가속

            else:  # 속력 810 이상
                if player.midair == 0:  # 접지
                    player.acc_x = vec(player.vel_x) * -(135 - s * 45)  # 이동방향이 같다면 -60, 다르다면 -150

                else:  # 체공
                    player.acc_x = vec(player.vel_x) * -(68.75 - s * 28.75)  # 이동방향이 같다면 -40, 다르다면 -97.5

                # player.acc_x = vec(player.vel_x) * 97.5 * -s # 이동방향이 같다면 감속, 아니라면 가속
                # player.acc_x = player.dir_x * -97.5 * s # 추가 감속

        # if game_framework.frame_time == 0:
        #     tick = 1
        # else:
        #     tick = (1/game_framework.frame_time) / 60

        # 60 프레임 기준으로 만든 코드를 변동 프레임 기준으로 바꾸어야 한다
        # 속도 및 가속도 둘 다 변경할 것.

        #print(game_framework.frame_rate)

        player.loc_x += player.vel_x * frame_time # 프레임당 속도(player.update가 초당 프레임 수만큼 실행되므로, 역산해서 더한다.)
        player.vel_x += player.acc_x # 프레임당 가속도

        # ===== Y 계산 =====

        if player.vel_y > 945:  # 상승 종단속도
            player.vel_y = 945

        if player.vel_y < -1440:  # 하강 종단속도
            player.vel_y = -1440

        player.loc_y += player.vel_y * frame_time #tick * game_framework.frame_time   # 프레임당 속도(player.update가 초당 프레임 수만큼 실행되므로, 역산해서 더한다.)
        player.vel_y += player.acc_y #60 * game_framework.frame_time#* tick  # 프레임당 가속도

        # 60 기준으로 만들어진 코드. 300프레임일 때 5배를 곱해야 한다.
        # ? 그럼 어케함?
        # 1/game_framework.frame_time  = 현재 프레임
        # 현재 프레임 / 60을 곱한다

        if player.loc_y > 150:  # 체공판별(임시)
            player.midair = 1

        elif player.loc_y < 150:  # 접지시
            player.loc_y = 150
            player.vel_y = 0
            player.acc_y = 0
            player.midair = 0

        if player.jump_time < 12 and player.press_space == 1:  # 점프 직후 점프키 홀딩시, 12프레임까지 가속도 감소 없음 < 0.2
            player.jump_time += 1 #game_framework.frame_time
            #player.jump_time += 1
            # print(jump_time)
            player.acc_y = 0

        elif player.midair == 1:  # 체공시
            if -405 < player.vel_y < 405 and player.press_space == 1:  # 최고점 근처에서 점프키 홀딩(감속 하강)
                player.acc_y = -67.5  # 중력 반감
            else:
                player.acc_y = -135  # 기본중력

        # if (abs(player.acc_y)) > 0:
        #     print(player.acc_y)

    def draw(player):
        if player.midair == 0:  # 접지시
            if player.dir_x == 0:  # 접지-정지
                player.image.clip_draw(46 - player.face_dir * 46, 200, 92, 100, player.loc_x, player.loc_y)
            else:  # 접지-이동
                player.image.clip_draw(player.frame * 92, 50 + player.face_dir * 50, 92, 100, player.loc_x, player.loc_y)
        else:  # 체공
            player.image.clip_draw(230 - player.face_dir * 46, 200, 92, 100, player.loc_x, player.loc_y)




# 대시 상태
class DASH_STATE:
    def enter(player, event):

        pass

    def exit(player, event):
        pass

    def do(player):
        pass

    def draw(player):
        player.image.clip_draw(230 - player.face_dir * 46, 200, 92, 100, player.loc_x, player.loc_y)
        #player.image.clip_draw(414 - player.face_dir * 46, 200, 92, 100, player.loc_x, player.loc_y)


# 대시 충돌 상태
#class DASH_COL_STATE:

# 사망
#class DIE_STATE

# 조건부로 진입해야함. lec12 boy파일의 timer를 응용해서 구현해보자
next_state_table = {
    MOVE_STATE:  {
        RIGHT_KD: MOVE_STATE,  LEFT_KD: MOVE_STATE,  UP_KD: MOVE_STATE,  DOWN_KD: MOVE_STATE, SPACE_KD: MOVE_STATE,
        RIGHT_KU: MOVE_STATE,  LEFT_KU: MOVE_STATE,  UP_KU: MOVE_STATE,  DOWN_KU: MOVE_STATE, SPACE_KU: MOVE_STATE,
        X_KD: DASH_STATE
        },
    DASH_STATE:   {
        RIGHT_KD: DASH_STATE,  LEFT_KD: DASH_STATE,  UP_KD: DASH_STATE,  DOWN_KD: DASH_STATE, SPACE_KD: DASH_STATE,
        RIGHT_KU: DASH_STATE,  LEFT_KU: DASH_STATE,  UP_KU: MOVE_STATE,  DOWN_KU: DASH_STATE, SPACE_KU: DASH_STATE,
        DASH_TIMER: MOVE_STATE}
}

class Player:

    def __init__(self):
        #self.x, self.y = 1280 // 2, 1024 // 2
        #self.dir = 1
        #self.x_vel, self.y_vel = 0, 0
        #self.frame = 0
        
        self.loc_x, self.loc_y = 200, 150 # x,y 위치
        self.vel_x, self.vel_y = 0, 0 # x,y 속도
        self.acc_x, self.acc_y = 0, 0 # x,y 가속도
        self.dir_x, self.dir_y = 0, 0  # x,y 방향키의 방향
        self.press_space, self.jump_time = 0, 0 # 스페이스 바 눌림, 점프 시간

        self.face_dir = 1 # 보고 있는 방향(좌 = -1, 우 = 1)
        self.midair = 0 # 접지 = 0, 체공 = 1
        self.frame = 0 # 현재 프레임 수
        self.dash_max = 1  # 연속으로 대시 가능한 횟수
        self.dash_count = 0  # 현재 남은 대시 가능한 횟수


        self.image = load_image('image/animation_sheet.png') # 이미지
        self.font = load_font('font/ENCR10B.TTF', 16) # 폰트

        self.event_que = []
        self.cur_state = MOVE_STATE # 현재 상태
        self.cur_state.enter(self, None)
        self.timer = 1000 # 타이머



    def get_bb(self):
        # fill here
        return self.loc_x - 30, self.loc_y - 50, self.loc_x + 30, self.loc_y + 40


    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)

        if self.event_que:
            event = self.event_que.pop()
            self.cur_state.exit(self, event) # self
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)


    def draw(self):
        self.cur_state.draw(self)
        self.font.draw(self.loc_x - 60, self.loc_y + 50, '%5d' % self.dash_count, (255, 255, 0))
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)


    # def handle_collision(self, other, group):
    #     if 'player:cristal' == group:
    #         self.dash_count = self.dash_max