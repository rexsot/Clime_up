from pico2d import *
import game_framework
import game_world
import server

from player import Player
from background_A1 import Background_A1
from gem import Gem_full
from plat_iron import Plat_iron
from strawberry import Strawberry_red, Strawberry_gold
from spike import Spike

frame_time = 0.013
background_A1 = None

gem_data = [
    {'x': 1530, 'y': 260},
    {'x': 600, 'y': 230},
    {'x': 700, 'y': 550}
]

plat_iron_data = [ # dir = -1일때 가로, dir = 1일때 세로
    {'x': 120, 'y': 419, 'dir': -1},
    {'x': 360, 'y': 419, 'dir': -1},

    {'x': 1800, 'y': 419, 'dir': -1},
    {'x': 2040, 'y': 419, 'dir': -1},

    {'x': 450, 'y': 269, 'dir': 1},
    {'x': 450, 'y': 29, 'dir': 1},


    {'x': 1710, 'y': 20, 'dir': 1}

]

strawberry_red_data = [
    {'x': 1300, 'y': 1000},
    {'x': 1830, 'y': 260}
]

strawberry_gold_data = [
    {'x': 1000, 'y': 50}
]

spike_data = [ # 상하좌우 -1234

    {'x': 1300, 'y': 420, 'dir': 1},
    {'x': 1300, 'y': 460, 'dir': 2},

    {'x': 1710, 'y': 364, 'dir': 1},

    {'x': 1100, 'y': 320, 'dir': 1},
    {'x': 1100, 'y': 360, 'dir': 2},

    {'x': 1100, 'y': 220, 'dir': 1},
    {'x': 1100, 'y': 260, 'dir': 2},

    {'x': 1100, 'y': 20, 'dir': 1},
    {'x': 1100, 'y': 60, 'dir': 2},

    {'x': 1100, 'y': 120, 'dir': 1},
    {'x': 1100, 'y': 160, 'dir': 2},

    {'x': 1000, 'y': 120, 'dir': 1},
    {'x': 1000, 'y': 160, 'dir': 2},

    {'x': 900, 'y': 120, 'dir': 1},
    {'x': 900, 'y': 160, 'dir': 2},

    {'x': 800, 'y': 120, 'dir': 1},
    {'x': 800, 'y': 160, 'dir': 2},

    {'x': 700, 'y': 120, 'dir': 1},
    {'x': 700, 'y': 160, 'dir': 2},


    {'x': 900, 'y': 390, 'dir': 1},
    {'x': 900, 'y': 430, 'dir': 2},

    {'x': 800, 'y': 390, 'dir': 1},
    {'x': 800, 'y': 430, 'dir': 2},

    {'x': 700, 'y': 390, 'dir': 1},
    {'x': 700, 'y': 430, 'dir': 2},

    {'x': 600, 'y': 390, 'dir': 1},
    {'x': 600, 'y': 430, 'dir': 2},



    {'x': 1710, 'y': 164, 'dir': 2},

    {'x': 504, 'y': 419, 'dir': 3},
    {'x': 504, 'y': 359, 'dir': 3},
    {'x': 504, 'y': 299, 'dir': 3},
    {'x': 504, 'y': 239, 'dir': 3},
    {'x': 504, 'y': 179, 'dir': 3},
    {'x': 504, 'y': 119, 'dir': 3},
    {'x': 504, 'y': 59, 'dir': 3},
    {'x': 504, 'y': -1, 'dir': 3}

]


# 초기화
def enter():
    global background_A1

    background_A1 = Background_A1()
    game_world.add_object(background_A1, 0) # 배경 오브젝트 추가

    server.player = Player()
    game_world.add_object(server.player, 1) # 플레이어 오브젝트 추가

    gems = [Gem_full(o['x'], o['y']) for o in gem_data]
    game_world.add_objects(gems, 1)

    plat_irons = [Plat_iron(o['x'], o['y'], o['dir']) for o in plat_iron_data]
    game_world.add_objects(plat_irons, 1)

    strawberrys_red = [Strawberry_red(o['x'], o['y']) for o in strawberry_red_data]
    game_world.add_objects(strawberrys_red, 1)

    strawberrys_gold = [Strawberry_gold(o['x'], o['y']) for o in strawberry_gold_data]
    game_world.add_objects(strawberrys_gold, 1)

    spikes = [Spike(o['x'], o['y'], o['dir']) for o in spike_data]
    game_world.add_objects(spikes, 1)

    game_world.add_collision_pairs(server.player, gems, 'player:gem_full')
    game_world.add_collision_pairs(server.player, plat_irons, 'player:plat_iron')
    game_world.add_collision_pairs(server.player, strawberrys_red, 'player:straw_red')
    game_world.add_collision_pairs(server.player, strawberrys_gold, 'player:straw_gold')
    game_world.add_collision_pairs(server.player, spikes, 'player:spike')


# 종료
def exit():
    game_world.clear()

def collide(a, b): # 맞닿을 시 충돌
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def update():
    delay(frame_time)
    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b): # == 1, == 2...로 구별가능
            b.handle_collision(a, group)
            a.handle_collision(b, group)

    for game_object in game_world.all_objects():
        game_object.update()


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
