from pico2d import *

# up/down - 상하좌우 및 스페이스(점프), down - 대시(x)
RIGHT_KEY_DOWN, LEFT_KEY_DOWN, UP_KEY_DOWN, DOWN_KEY_DOWN = range(4)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RD,
    (SDL_KEYDOWN, SDLK_LEFT): LD,
    (SDL_KEYUP, SDLK_RIGHT): RU,
    (SDL_KEYUP, SDLK_LEFT): LU
}

class RUN:
    @staticmethod
    def enter():
        pass

    @staticmethod
    def exit():
        pass

    @staticmethod
    def do():
        pass

    @staticmethod
    def draw():
        pass

class DASH:
    @staticmethod
    def enter():
        pass

    @staticmethod
    def enter():
        pass

    @staticmethod
    def enter():
        pass

    @staticmethod
    def enter():
        pass
