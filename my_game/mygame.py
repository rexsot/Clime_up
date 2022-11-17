import pico2d

import game_framework
import play_state
#import play_state
#import item_state

#X_MAX = 1920
#Y_MAX = 1080


X_MAX = 910
Y_MAX = 540


pico2d.open_canvas(X_MAX, Y_MAX)
game_framework.run(play_state) #logo_state
pico2d.close_canvas()
