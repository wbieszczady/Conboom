import pyglet, time

class Texture:
    def __init__(self):

        self.all = {'placeholder': pyglet.image.load('resources/gui/placeholder.png'),
                    'placeholder_selected': pyglet.image.load('resources/gui/placeholder_selected.png'),
                    'background': pyglet.image.load('resources/gui/mainMenu.png'),

                    'border': pyglet.image.load('resources/game/border.png'),
                    'playground': pyglet.image.load('resources/game/playground.png'),
                    'crate': pyglet.image.load('resources/game/crate.png'),
                    'speed': pyglet.image.load('resources/game/speed.png'),
                    'force': pyglet.image.load('resources/game/force.png'),

                    'dynamite': pyglet.image.load('resources/player/dynamite.png'),
                    'explosion': pyglet.image.Animation.from_image_sequence(pyglet.image.ImageGrid(pyglet.image.load('resources/player/explosion.png'), rows=1, columns=11), duration=0.05),
                    'right-walk': pyglet.image.Animation.from_image_sequence(pyglet.image.ImageGrid(pyglet.image.load('resources/player/right-walk.png'), rows=1, columns=2), duration=0.1),
                    'left-walk': pyglet.image.Animation.from_image_sequence(pyglet.image.ImageGrid(pyglet.image.load('resources/player/left-walk.png'), rows=1, columns=2), duration=0.1),
                    'right-idle': pyglet.image.load('resources/player/right-idle.png'),
                    'left-idle': pyglet.image.load('resources/player/left-idle.png')
                    }

class Sound:
    def __init__(self, game):

        self.volume = game.cfg.master_volume

        self.all = {'click': pyglet.media.load(f'resources/sound/console.wav', streaming=False),
                    'success': pyglet.media.load(f'resources/sound/console-success.mp3', streaming=False),
                    'failure': pyglet.media.load(f'resources/sound/console-failure.mp3', streaming=False),
                    'startup': pyglet.media.load(f'resources/sound/console-startup.mp3', streaming=False),
                    'enter': pyglet.media.load('resources/sound/console-enter.mp3', streaming=False)}

    def play(self, sound):
        self.all[sound].play().volume = float(self.volume)