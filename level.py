import random
import pyglet, time, builtins
from tiles import Border, Floor, Crate, Explosion
from entity import Player
from gui import Button
from util import *
from threading import Thread
import pymunk
from pymunk.pyglet_util import DrawOptions

class LoadingScreen:
    def __init__(self, game):
        self.game = game

        self.maxWidth = 790
        self.elements = 2

        self.frame = pyglet.shapes.Box(game.width // 2 - 400, game.height // 2 - 50, 800, 100, 1, color=[255, 255, 255, 255], batch=game.batch)
        self.bar = pyglet.shapes.Rectangle(game.width // 2 - 395, game.height // 2 - 45, 0, 90, color=[255, 255, 255, 255], batch=game.batch)
        self.percent = pyglet.text.Label('Loading Textures...', color=[255, 255, 255, 255], font_size=24, font_name='BN Machine', x=game.width // 2,
                                           y=game.height // 2 - 80, anchor_x='center', anchor_y='center', batch=game.batch)

        pyglet.clock.schedule_interval(self.init_load, 1/60)

    def init_load(self, dt):

        self.bar.width += random.randint(0, 7000) * dt

        if self.bar.width >= self.maxWidth-6:
            pyglet.clock.unschedule(self.init_load)
            self.game.clear_batch()
            self.game.load_resources()
            self.game.get_menu()


class Menu:

    def __init__(self, game):

        self.game = game
        self.textures = game.textures.all

        self.value = 0

        self.mainBackground = pyglet.sprite.Sprite(img=self.textures['background'], x=0, y=0, batch=game.batch)
        self.mainBackground.width, self.mainBackground.height = game.width, game.height

        self.mainLabel = pyglet.text.Label('<game-title>', color=[255, 255, 255, 255], font_size=74, font_name='BN Machine',x=game.width // 2,
                                           y=game.height // 2 + 300, anchor_x='center', anchor_y='center', batch=game.batch)

        self.buttons = [Button(self, game.height // 2 + 40, 'Singleplayer', self.textures['placeholder'], self.textures['placeholder_selected']),
                        Button(self, game.height // 2 - 80, 'Multiplayer', self.textures['placeholder'], self.textures['placeholder_selected']),
                        Button(self, game.height // 2 - 200, 'Settings', self.textures['placeholder'], self.textures['placeholder_selected']),
                        Button(self, game.height // 2 - 320, 'Quit', self.textures['placeholder'], self.textures['placeholder_selected'])]

        self.selector(self.value)

    def selector(self, incr):

        val = self.value + incr

        if val in range(0, 4):
            self.value = val
            for b in self.buttons:
                b.deselect()
            self.buttons[self.value].select()
class Settings:
    def __init__(self, game):
        self.game = game
        self.textures = game.textures.all

        self.mainBackground = pyglet.sprite.Sprite(img=self.textures['background'], x=0, y=0, batch=game.batch)
        self.mainBackground.width, self.mainBackground.height = game.width, game.height

        width = game.width // 1.5
        height = game.height // 1.5

        self.box = pyglet.shapes.Rectangle(game.width // 2 - width // 2, game.height // 2 - height // 2, width, height, color=[0, 0, 0, 255], batch=game.batch)
        self.windowLabel = pyglet.text.Label(text=WELCOME, font_name = 'BN Machine', font_size = 29, color = [255, 255, 255, 255], x = self.box.x + 35, y = self.box.y + self.box.height - 70, batch = game.batch, multiline=True, width=width - 70, height=height-70)

        self.terminal = pyglet.shapes.Rectangle(game.width // 2 - width // 2, game.height // 2 - height // 2, width, 70, color=[10, 10, 10, 255], batch=game.batch)
        self.mainLabel = pyglet.text.Label('> ', color=[255, 255, 255, 255], font_name='BN Machine', font_size=34, x=self.terminal.x + 20, y=self.terminal.y + 20, batch=game.batch)
        self.commandLabel = pyglet.text.Label('', color=[255, 255, 255, 255], font_name='BN Machine', font_size=34, x=self.terminal.x + 60, y=self.terminal.y + 20, batch=game.batch)

        self.keys = pyglet.window.key.KeyStateHandler()
        game.push_handlers(self.keys)
        pyglet.clock.schedule_interval(self.on_press, 1/10)

    def on_press(self, dt):
        if self.keys[pyglet.window.key.BACKSPACE]:
            self.remove_text()

    def apply_command(self):

        config = self.game.cfg
        command = resemblance(self.commandLabel.text)
        self.windowLabel.color = (255, 255, 255, 255)

        match command:

            case 'help':
                self.game.sounds.play('enter')
                self.windowLabel.text = HELP
            case 'settings':
                self.game.sounds.play('enter')
                self.windowLabel.text = config.SETTINGS()

            case 'master volume':
                self.game.sounds.play('enter')
                self.windowLabel.text = config.MASTER_VOLUME()
            case int():
                if self.windowLabel.text == config.MASTER_VOLUME():
                    config.master_volume = int(self.commandLabel.text) / 100
                    self.game.sounds.volume = config.master_volume
                    self.windowLabel.text = config.MASTER_VOLUME()
                    self.game.sounds.play('success')
                else:
                    self.console_error(f"Couldn't recognize command '{self.commandLabel.text}'")
            case 'confirm':
                if self.windowLabel.text == config.MASTER_VOLUME():
                    self.game.sounds.play('success')
                    self.windowLabel.text = config.SETTINGS()
                else:
                    self.console_error(f"Couldn't recognize command '{self.commandLabel.text}'")

            case 'fullscreen':
                self.game.sounds.play('success')

                self.game.clear_batch()
                config.fullscreen = True if config.fullscreen == False else False
                self.game.reset_resolution()
                self.game.get_settings()
                self.game.settings.windowLabel.text = config.SETTINGS()
            case 'vsync':
                self.game.sounds.play('success')
                config.vsync = True if config.vsync == False else False
                self.game.settings.windowLabel.text = config.SETTINGS()
            case 'fps counter':
                self.game.sounds.play('success')
                config.fps_counter = True if config.fps_counter == False else False
                self.game.settings.windowLabel.text = config.SETTINGS()

            case 'resolution':
                if config.fullscreen == False:
                    self.game.sounds.play('success')
                    self.windowLabel.text = config.RESOLUTION()
                else:
                    self.console_error(f"Can't change resolution with fullscreen turned on.")
            case '1280x720':
                if self.windowLabel.text == config.RESOLUTION():
                    self.game.sounds.play('success')
                    self.game.clear_batch()
                    config.width, config.height = 1280, 720
                    self.game.width, self.game.height = 1280, 720
                    self.game.get_settings()
                    self.game.settings.windowLabel.text = config.SETTINGS()
                else:
                    self.console_error(f"Couldn't recognize command '{self.commandLabel.text}'")
            case '1920x1080':
                if self.windowLabel.text == config.RESOLUTION():
                    self.game.sounds.play('success')
                    self.game.clear_batch()
                    config.width, config.height = 1920, 1080
                    self.game.width, self.game.height = 1920, 1080
                    self.game.get_settings()
                    self.game.settings.windowLabel.text = config.SETTINGS()
                else:
                    self.console_error(f"Couldn't recognize command '{self.commandLabel.text}'")
            case '2560x1440':
                if self.windowLabel.text == config.RESOLUTION():
                    self.game.sounds.play('success')
                    self.game.clear_batch()
                    config.width, config.height = 2560, 1440
                    self.game.width, self.game.height = 2560, 1440
                    self.game.get_settings()
                    self.game.settings.windowLabel.text = config.SETTINGS()
                else:
                    self.console_error(f"Couldn't recognize command '{self.commandLabel.text}'")
            case _:
                self.console_error(f"Couldn't recognize command '{self.commandLabel.text}'")


        self.commandLabel.text = ''

    def change_text(self, code):
        if len(self.commandLabel.text) < 20:
            if code == 'SPACE':
                self.commandLabel.text += ' '
            else:
                self.commandLabel.text += str(code).lower()
    def remove_text(self):
        if self.commandLabel.text != '':
            self.game.sounds.play('click')
            self.commandLabel.text = self.commandLabel.text[:-1]

    def console_error(self, message):
        self.game.sounds.play('failure')
        self.windowLabel.text = message
        self.windowLabel.color = (255, 0, 0, 255)

class Singleplayer:
    def __init__(self, game):

        self.game = game
        self.offset = game.offset

        self.objects = []
        self.crates = []
        self.powerups = []
        self.create_map()

        self.spawn_player(64, 64)

    def create_map(self):

        for yindex, y in enumerate(MAP):
            for xindex, x in enumerate(y):
                xpos, ypos = xindex * 64, yindex * 64

                if x == 'x':
                    b = Border(self, xpos, ypos)
                    self.objects.append(b)
                elif x == 'o':
                    Floor(self, xpos, ypos)
                elif x == 'c':
                    Floor(self, xpos, ypos)
                    c = Crate(self, xpos, ypos)
                    self.objects.append(c)
                    self.crates.append(c)

    def spawn_explosion(self, x, y):
        e = Explosion(self, x, y)
    def spawn_player(self, x, y):
        self.player = Player(self, x, y)
        self.player.center_camera()