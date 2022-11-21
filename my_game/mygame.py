import pico2d
import game_framework
import play_state
#import play_state
#import item_state

#X_MAX = 1920
#Y_MAX = 1080


game_framework.X_MAX = 910
game_framework.Y_MAX = 540

pico2d.open_canvas(game_framework.X_MAX, game_framework.Y_MAX)
game_framework.run(play_state) #logo_state
pico2d.close_canvas()
