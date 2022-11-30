from pico2d import *
import game_framework

from player import Player

frame_time = 0.013


player = None
#grass = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        else:
            player.handle_event(event)


# 초기화
def enter():
    global player#, grass
    player = Player()
    #grass = Grass()

# 종료
def exit():
    global player#, grass
    del player
    #del grass

def update():
    delay(frame_time)
    player.update()

def draw_world():
    #grass.draw()
    player.draw()

def draw():
    clear_canvas()
    draw_world()
    update_canvas()

def pause():
    pass

def resume():
    pass

def test_self():
    import play_state2

    pico2d.open_canvas()
    game_framework.run(play_state2)
    pico2d.clear_canvas()

if __name__ == '__main__':
    test_self()
