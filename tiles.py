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

        self.texture = level.game.textures.all
        self.texture = self.texture['crate']

        super().__init__(img=self.texture, batch=level.game.batch, group=level.game.background, x=x, y=y)
        pyglet.clock.schedule_interval(self.update, 1)

    def update(self, dt):
        pass

    def die(self):
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


