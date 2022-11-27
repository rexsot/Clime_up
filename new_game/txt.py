player.frame = (player.frame + 1) % 20  # 프레임 계산

# 보는 방향 판별
if player.dir_x > 0:
    player.face_dir = 1
if player.dir_x < 0:
    player.face_dir = -1

# if (0 < player.loc_x + player.dir_x * 9 and player.loc_x + player.dir_x * 9 < X_MAX): # x좌표 제한
#     player.loc_x += player.dir_x * 9 # x축 이동


# X 계산

# 속도의 방향(vel_x)과 키의 방향(dir_x)이 일치할 때 덜 감속하고, 불일치할 때(방향키가 중립일 때 포함) 더 감속한다.
s = sig(player.dir_x, player.vel_x)  # 방향과 속도가 같다면 1, 아니면 -1
vel_x_abs = abs(player.vel_x)  # x 속도의 절댓값(속력)

if player.dir_x == 0:  # 방향키가 중립일 때
    if vel_x_abs <= 97.5:  # 최소 속력이하 - 정지
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

player.loc_x += player.vel_x * frame_time  # 프레임당 속도(player.update가 초당 프레임 수만큼 실행되므로, 역산해서 더한다.)
player.vel_x += player.acc_x  # 프레임당 가속도

# Y 계산

if player.vel_y > 945:  # 상승 종단속도
    player.vel_y = 945

if player.vel_y < -1440:  # 하강 종단속도
    player.vel_y = -1440

player.loc_y += player.vel_y * frame_time  # 프레임당 속도(player.update가 초당 프레임 수만큼 실행되므로, 역산해서 더한다.)
player.vel_y += player.acc_y  # 프레임당 가속도

if player.loc_y > 150:  # 체공판별(임시)
    player.midair = 1

elif player.loc_y < 150:  # 접지시
    player.loc_y = 150
    player.vel_y = 0
    player.acc_y = 0
    player.midair = 0

if player.jump_time < 12 and player.press_space == 1:  # 점프 직후 점프키 홀딩시, 12프레임까지 가속도 감소 없음
    player.jump_time += 1
    # print(jump_time)
    player.acc_y = 0

elif player.midair == 1:  # 체공시
    if -405 < player.vel_y < 405 and player.press_space == 1:  # 최고점 근처에서 점프키 홀딩(감속 하강)
        player.acc_y = -67.5  # 중력 반감
    else:
        player.acc_y = -135  # 기본중력

# if (abs(player.acc_y)) > 0:
#     print(player.acc_y)