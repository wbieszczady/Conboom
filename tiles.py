import random

import pyglet, pymunk

class Border(pyglet.sprite.Sprite):

    def __init__(self, level, x, y):

        self.textures = level.game.textures.all

        self.texture = self.textures['border']

        super().__init__(img=self.texture, batch=level.game.batch, group=level.game.background, x=x, y=y)
        pyglet.clock.schedule_interval(self.update, 1)

    def update(self, dt):
        pass

class Floor(pyglet.sprite.Sprite):

    def __init__(self, level, x, y):

        self.textures = level.game.textures.all

        self.texture = self.textures['playground']

        super().__init__(img=self.texture, batch=level.game.batch, group=level.game.background, x=x, y=y)
        pyglet.clock.schedule_interval(self.update, 1)

    def update(self, dt):
        pass

class Crate(pyglet.sprite.Sprite):

    def __init__(self, level, x, y):
        self.level = level

        self.textures = level.game.textures.all
        self.texture = self.textures['crate']

        super().__init__(img=self.texture, batch=level.game.batch, group=level.game.background, x=x, y=y)
        pyglet.clock.schedule_interval(self.update, 1)

    def update(self, dt):
        pass

    def get_random_powerup(self):
        i = random.randint(1, 2)

        if i == 1:
            s = Power(self.level, self.x, self.y, 'speed')
        else:
            s = Power(self.level, self.x, self.y, 'force')

        self.level.powerups.append(s)

    def die(self):
        self.get_random_powerup()
        self.level.crates.remove(self)
        self.level.objects.remove(self)
        self.delete()
        del self

class Explosion(pyglet.sprite.Sprite):

    def __init__(self, level, x, y):

        self.level = level

        self.textures = level.game.textures.all
        self.texture = self.textures['explosion']

        self.duration = self.texture.get_duration()

        super().__init__(img=self.texture, batch=level.game.batch, group=level.game.background, x=x, y=y)
        pyglet.clock.schedule_interval(self.update, self.duration)
        pyglet.clock.schedule_interval(self.collision, 1/60)

    def update(self, dt):
        pyglet.clock.unschedule(self.collision)
        pyglet.clock.unschedule(self.update)
        self.delete()

    def collision(self, dt):

        player = self.level.player

        if player:
            if self.x < player.x+16 + player.width-32 and self.x + self.width > player.x+16 and self.y < player.y + player.height//3 and self.y + self.height > player.y:
                player.die()

        for crate in self.level.crates:
            if self.x < crate.x + crate.width and self.x + self.width > crate.x and self.y < crate.y + crate.height and self.y + self.height > crate.y:
                crate.die()

class Power(pyglet.sprite.Sprite):
    def __init__(self, level, x, y, type):

        self.type = type

        self.textures = level.game.textures.all
        self.texture = self.textures[type]

        super().__init__(img=self.texture, batch=level.game.batch, group=level.game.background, x=x+16, y=y+16)
        pyglet.clock.schedule_interval(self.update, 1)

    def update(self, dt):
        pass