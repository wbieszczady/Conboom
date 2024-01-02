import pyglet
from tiles import Border, Explosion
from util import *

class Dynamite(pyglet.sprite.Sprite):

    def __init__(self, player, cooldown, force):

        self.game = player.game
        self.player = player

        self.texture = self.game.textures.all['dynamite']

        # self.texture = self.textures['dynamite']

        x = int(player.x) + self.player.width//2 - self.texture.width//2
        y = int(player.y)

        self.cooldown = cooldown
        self.force = force

        super().__init__(img=self.texture, x=x, y=y, batch=self.game.batch, group=self.game.background)
        pyglet.clock.schedule_interval(self.update, 1/60)

    def update(self, dt):

        self.cooldown -= 10 * dt
        if self.cooldown < 0:
            self.explode()

    def explode(self):
        pyglet.clock.unschedule(self.update)

        xindex = (self.x + self.width//2)//64
        yindex = (self.y + self.height//2)//64

        #initial explosion
        self.player.level.spawn_explosion(xindex*64, yindex*64)

        dic = {'top': True,
               'right': True,
               'left': True,
               'bottom': True}

        xi = 1
        yi = 1

        while True:

            rightx = (xindex+xi) * 64
            righty = yindex * 64
            leftx = (xindex-xi) * 64
            lefty = yindex * 64
            topx = xindex * 64
            topy = (yindex+yi) * 64
            bottomx = xindex * 64
            bottomy = (yindex-yi) * 64

            if dic['right'] == True:
                if MAP[xindex+xi][yindex] != 'x':
                    self.player.level.spawn_explosion(rightx, righty)
                    self.force -= 1
                else:
                    self.force -= 1
                    dic['right'] = False


            if dic['left'] == True:
                if MAP[xindex-xi][yindex] != 'x':
                    self.player.level.spawn_explosion(leftx, lefty)
                    self.force -= 1
                else:
                    self.force -= 1
                    dic['left'] = False

            if dic['top'] == True:
                if MAP[xindex][yindex+yi] != 'x':
                    self.player.level.spawn_explosion(topx, topy)
                    self.force -= 1
                else:
                    self.force -= 1
                    dic['top'] = False


            if dic['bottom'] == True:
                if MAP[xindex][yindex-yi] != 'x':
                    self.player.level.spawn_explosion(bottomx, bottomy)
                    self.force -= 1
                else:
                    self.force -= 1
                    dic['bottom'] = False

            if self.force <= 0:
                break

            f = [m for m in dic.values()]
            if f.count(False) == len(dic):
                break

            xi += 1
            yi += 1

        self.delete()