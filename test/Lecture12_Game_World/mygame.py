import game_framework
import pico2d
import play_state

X_MAX = 1920
Y_MAX = 1080

pico2d.open_canvas(X_MAX, Y_MAX)
game_framework.run(play_state)
pico2d.close_canvas()