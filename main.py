import random

import pyglet, math
import time
from entity import Player
from level import Menu, LoadingScreen, Settings, Singleplayer
import pymunk
from pymunk.pyglet_util import DrawOptions
from pyglet.window import key
from resources import Texture, Sound
from threading import Thread
from util import *


class Game(pyglet.window.Window):
    def __init__(self):
        super().__init__()

        self.cfg = Config(self)

        pyglet.options['win32_gdi_font'] = True
        pyglet.font.add_file("BNMachine.ttf")
        BNMachine = pyglet.font.load("BN Machine", 16)

        self.view = self.view.from_translation(pyglet.math.Vec3(0, 0, 0))

        self.fps = pyglet.window.FPSDisplay(window=self)
        self.offset = [0, 0]

        self.clear_batch()
        self.loading = LoadingScreen(self)

    def on_draw(self):

        self.clear()
        self.batch.draw()

        if self.cfg.fps_counter:
            self.fps.draw()

    def on_key_press(self, symbol, modifiers):

        if self.menu:
            if symbol == key.UP:
                self.menu.selector(-1)

            if symbol == key.DOWN:
                self.menu.selector(1)

            if symbol == key.ENTER:

                match self.menu.value:
                    case 3:
                        pyglet.app.exit()
                    case 2:
                        self.sounds.play('startup')
                        self.clear_batch()
                        self.get_settings()
                    case 0:
                        self.clear_batch()
                        self.get_singleplayer()

        if self.settings:

            if symbol == key.ESCAPE:
                self.clear_batch()
                self.get_menu()
            if symbol == key.ENTER and self.settings.commandLabel.text != '':
                self.settings.apply_command()

            if symbol in CODES:
                self.sounds.play('click')
                self.settings.change_text(key.symbol_string(symbol))
            if symbol in CODES_L:
                self.sounds.play('click')
                string = key.symbol_string(symbol)[1:]
                self.settings.change_text(string)

    def clear_batch(self):

        self.reset_resolution()
        self.batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.Group(0)
        self.foreground = pyglet.graphics.Group(1)
        self.gui = pyglet.graphics.Group(2)

    def reset_resolution(self):
        if self.cfg.fullscreen == False:
            self.set_size(int(self.cfg.width), int(self.cfg.height))

        self.menu = self.loading = self.settings = self.singleplayer = None
    def load_resources(self):
        self.textures = Texture()
        self.sounds = Sound(self)
    def get_menu(self):
        self.menu = Menu(self)
    def get_lscreen(self):
        self.loading = LoadingScreen(self)
    def get_settings(self):
        self.settings = Settings(self)
    def get_singleplayer(self):
        self.singleplayer = Singleplayer(self)
    def set_camera(self, x=0, y=0):
        self.fps.label.x = -x+10
        self.fps.label.y = -y+10
        self.game_gui(x, y)
        self.view = self.view.from_translation(pyglet.math.Vec3(x, y, 0))

    def game_gui(self, x, y):
        if self.singleplayer:
            self.singleplayer.player.gui.bombIcon.x = -x+self.width//2-32
            self.singleplayer.player.gui.bombIcon.y = -y+30
            self.singleplayer.player.gui.bombBar.x = -x+self.width//2-32
            self.singleplayer.player.gui.bombBar.y = -y+30

if __name__ == "__main__":
    app = Game()
    pyglet.app.run(interval=0)