import random
import pyglet
from projectiles import Dynamite
from pyglet.window import key
from pyglet.gl import gl
from gui import Gui
import pymunk

class Player(pyglet.sprite.Sprite):
    def __init__(self, level, x, y):

        self.level = level
        self.game = level.game
        self.offset = level.offset

        #gui
        self.gui = Gui(self)
        self.bombMax = self.gui.bombBar.width
        self.bomb = self.bombMax

        #textures
        self.textures = self.game.textures.all
        self.dir = 'right-idle'
        self.texture = self.textures[f'{self.dir}']

        self.keys = key.KeyStateHandler()
        self.level.game.push_handlers(self.keys)

        #bomb cooldown
        self.ready = True
        self.bombMax = self.gui.bombBar.width
        self.bomb = self.bombMax

        self.speed = 130
        self.force = 4

        super().__init__(img=self.texture, batch=level.game.batch, group=level.game.foreground, x=x, y=y)
        pyglet.clock.schedule_interval(self.update, 1/60)

    def update(self, dt):

        if self.dir == 'right-walk':
            direction = 'right-idle'
        elif self.dir == 'left-walk':
            direction = 'left-idle'
        else:
            direction = None

        if self.keys[key.A]:
            self.x += -self.speed * dt
            self.offset[0] += self.speed * dt
            self.check_collision('left', dt)
            direction = 'left-walk'
        elif self.keys[key.D]:
            self.x += self.speed * dt
            self.offset[0] += -self.speed * dt
            self.check_collision('right', dt)
            direction = 'right-walk'

        if self.keys[key.W]:
            self.y += self.speed * dt
            self.offset[1] += -self.speed * dt
            self.check_collision('top', dt)
            direction = 'right-walk'

        elif self.keys[key.S]:
            self.y += -self.speed * dt
            self.offset[1] += self.speed * dt
            self.check_collision('bottom', dt)
            direction = 'left-walk'

        if self.keys[key.A] and (self.keys[key.W] or self.keys[key.S]):
            direction = 'left-walk'
        elif self.keys[key.D] and (self.keys[key.W] or self.keys[key.S]):
            direction = 'right-walk'

        self.animate(direction)

        self.game.set_camera(self.offset[0], self.offset[1])

        if self.keys[key.SPACE] and self.ready:
            Dynamite(self, cooldown=20, force=self.force)
            self.ready = False
            pyglet.clock.schedule_interval(self.cooldown, 1/60)

    def cooldown(self, dt):
        self.gui.bombBar.width -= 100 * dt
        self.gui.bombBar.color = (255, 255, 255, 100)
        if self.gui.bombBar.width < 0:
            self.ready = True
            self.gui.bombBar.color = (255, 255, 255, 0)
            self.gui.bombBar.width = self.bombMax
            pyglet.clock.unschedule(self.cooldown)

    def animate(self, direction):
        if self.dir == direction:
            pass
        elif direction == None:
            pass
        else:
            self.dir = direction
            self.image = self.textures[self.dir]

    def center_camera(self):
        self.offset[0] = -self.x + self.game.width//2 - self.width//2
        self.offset[1] = -self.y + self.game.height//2 - self.height//2
        self.game.set_camera(self.offset[0], self.offset[1])

    def bounce(self, side, dt):

        if side == 'left':
            self.x += self.speed * dt
            self.offset[0] += -self.speed * dt
        elif side == 'right':
            self.x += -self.speed * dt
            self.offset[0] += self.speed * dt
        elif side == 'top':
            self.y += -self.speed * dt
            self.offset[1] += self.speed * dt
        elif side == 'bottom':
            self.y += self.speed * dt
            self.offset[1] += -self.speed * dt

    def check_collision(self, side, dt):
        for obst in self.level.objects:
            if self.x+16 < obst.x + obst.width and self.x+16 + self.width-32 > obst.x and self.y < obst.y + obst.height and self.y + (self.height//3) > obst.y:
                self.bounce(side, dt)

        for power in self.level.powerups:
            if self.x+16 < power.x + power.width and self.x+16 + self.width-32 > power.x and self.y < power.y + power.height and self.y + (self.height//3) > power.y:

                if power.type == 'speed':
                    self.speed += 10
                if power.type == 'force':
                    self.force += 1

                self.level.powerups.remove(power)
                power.delete()


    def die(self):
        pyglet.clock.unschedule(self.update)
        self.level.player = None
        self.delete()
        del self