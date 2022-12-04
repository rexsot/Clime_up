from pico2d import *
import game_framework
import game_world
import server

from player import Player
from background_A1 import Background_A1

frame_time = 0.013
background_A1 = None

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

# 초기화
def enter():
    global background_A1

    background_A1 = Background_A1()
    server.player = Player()

    game_world.add_object(background_A1, 0) # 플레이어 오브젝트 추가
    game_world.add_object(server.player, 0) # 플레이어 오브젝트 추가


# 종료
def exit():
    game_world.clear()

def update():
    delay(frame_time)
    for game_object in game_world.all_objects():
        game_object.update()

    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b):
            print('COLLISION ', group)
            a.handle_collision(b, group)
            b.handle_collision(a, group)

def draw_world():
    for game_object in game_world.all_objects():
        game_object.draw()

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()

def pause():
    pass

def resume():
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        else:
            server.player.handle_event(event)

# def test_self():
#     import play_state
#     pico2d.open_canvas()
#     game_framework.run(play_state)
#     pico2d.clear_canvas()

# if __name__ == '__main__':
#     test_self()
