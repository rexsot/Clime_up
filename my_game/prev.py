from pico2d import *

# 화면 크기
X_MAX = 1920 
Y_MAX = 1080

open_canvas(X_MAX, Y_MAX)

#이미지
background = load_image('background.png')
character = load_image('animation_sheet.png')
ice = load_image('plat_ice.png')
iron = load_image('plat_iron.png')

#장애물 - 좌표

pos = []


ICE_pos_x = [150, 450, 750, 1770]
ICE_pos_y = [50, 50, 50, 50]
IRON_pos_x = [300, 1100, 1500, 1700]
IRON_pos_y = [250, 150, 250, 450]

running = True

grounded = 0; #접지 함수

x = 200 # 캐릭터 x
y = 150 # 캐릭터 y

vec_x = 0 # x 속도
vec_y = 0 # y 속도
vec_y_f = 0 # y 가속도

sel = 1 # 이미지 방향
frame = 0  # 이미지 프레임

press_space = 0 # 스페이스바 키가 눌려있으면 1, 아니면 0

jump_timer = 12

def handle_events():
    global running
    global x
    global y
    global vec_x
    global vec_y
    global vec_y_f
    global sel
    global press_space
    
    events = get_events()
    
    for event in events:
        if event.type == SDL_QUIT: #창닫기
            running = False
            
        elif event.type == SDL_KEYDOWN: # 키 누를때
            if event.key == SDLK_ESCAPE: #esc
                running = False
            elif event.key == SDLK_RIGHT:
                vec_x += 1
            elif event.key == SDLK_LEFT:
                vec_x -= 1
            if event.key == SDLK_SPACE:
                press_space = 1 #스페이스바가 눌려있을 때
                if grounded == 0:  #접지중 점프시
                    vec_y_f = 945



                
        elif event.type == SDL_KEYUP: #키 땔때
            if event.key == SDLK_RIGHT:
                vec_x -= 1
            elif event.key == SDLK_LEFT:
                vec_x += 1
            if event.key == SDLK_SPACE: # 스페이스바가 때질 때
                press_space = 0 
                if grounded == 1: # 공중일 경우 
                    if (vec_y > 0): # 상승중일 때 즉시 추락 시작
                        vec_y = 0 
                   

    
while running:
    clear_canvas()
    background.draw(X_MAX/2, Y_MAX/2) #배경
    
    #장애물 출력    
    for i in range(len(ICE_pos_x)):
        ice.draw(ICE_pos_x[i], ICE_pos_y[i])
        
    for i in range(len(IRON_pos_x)):
        iron.draw(IRON_pos_x[i], IRON_pos_y[i])


    # 캐릭터 모션 출력
    if grounded == 0: #접지시 
        if vec_x == 0: #접지-이동시
            if sel == 1:
                character.clip_draw(0, 200, 92, 100, x, y)
            else:
                character.clip_draw(92, 200, 92, 100, x, y)
        else: #접지-정지시
            character.clip_draw(frame * 92, sel * 100, 92, 100, x, y)
    else: #체공시
        if sel == 1: 
                character.clip_draw(194, 200, 92, 100, x, y)
        else:
            character.clip_draw(286, 200, 92, 100, x, y)
        
    update_canvas()
    handle_events()
    
    if (vec_x > 0): #좌우판별
        sel = 1
    elif (vec_x < 0):
        sel = 0

    if y > 150: #중력
        grounded = 1
        if vec_y > -405 and press_space == 1: # 추락속도 405이하, 점프키 누르기(감속 하강)
            vec_y_f -= 67.5
        else: #그외
            vec_y_f -= 135
            

    if vec_y < -1440: #종단속도
        vec_y = -1440
        vec_y_f = 0

    if vec_y > 1440: #공기저항(상승 종단 속도)
        vec_y = 1440

    if y < 150: #접지
        grounded = 0
        vec_y = 0
        vec_y_f = 0
        y = 150

    y += vec_y * 0.015 #위치 += 속도
    vec_y += vec_y_f # 속도 += 가속도
    jump_timer += 1
    
    if (0 < x + vec_x * 10 and x + vec_x * 10 < X_MAX):
        x += vec_x * 10

    frame = (frame + 1) % 20
    delay(0.017)

close_canvas()
