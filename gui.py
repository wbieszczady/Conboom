import pyglet
from pyglet.window import mouse

class Gui:
    def __init__(self, player):

        self.level = player.level
        self.game = player.game

        bombIcon = pyglet.image.load('resources/gui/dynamiteIcon.png')

        self.bombIcon = pyglet.sprite.Sprite(img=bombIcon, x=self.game.width//2-32, y=30, batch=self.game.batch, group=self.game.gui)
        self.bombBar = pyglet.shapes.Rectangle(x=self.game.width//2-32, y=30, width=64, height=64, batch=self.game.batch, group=self.game.gui, color=(255, 255, 255, 0))

class Button(pyglet.sprite.Sprite):

    def __init__(self, level, y, label, txt1, txt2):

        self.txt1 = txt1
        self.txt2 = txt2
        self.level = level

        x = (level.game.width // 2) - (txt1.width // 2)

        self.label = pyglet.text.Label(label, color=[255, 255, 255, 255], font_size=24,
                                       x=x + 155,
                                       y=y + 55,
                                       anchor_x='center',
                                       anchor_y='center',
                                       font_name='BN Machine',
                                       batch=level.game.batch)

        super().__init__(img=txt1, x=x, y=y, batch=level.game.batch)

    def select(self):
        self.image = self.txt2

    def deselect(self):
        self.image = self.txt1
