from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.properties import ListProperty, StringProperty
from kivy.uix.widget import Widget
from random import randint

class Platform(Widget):
    velocity = ListProperty([0, 0])
    image_source = StringProperty('nuvem_1.png')

    def __init__(self, player, isBooster, **kwargs):
        super(Platform, self).__init__(**kwargs)
        self.pos = kwargs['pos']
        self.size = kwargs['size']
        self.player = player
        self.isBooster = isBooster
        self.paused = False
        self.background_movement_speed = 20

    def update(self, *args):
        if self.paused:
            return

        self.platform_player_collision()
        if self.player.boost_active:
            self.boost_platform()
        else:
            self.move_platform()
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.draw()

    def draw(self, *args):
        self.canvas.clear()
        with self.canvas:
            if not self.isBooster:
                self.image_source = str('nuvem_1.png')
            else:
                self.image_source = str('boost.png')
            Rectangle(pos=self.pos, size=(175, 80), source=(self.image_source))

    def platform_player_collision(self):
        # check player collision with platforms
        if self.player.collide_widget(self):
            if self.player.velocity[1] < -5 and self.player.pos[1] > self.pos[1] - self.height / 2 \
                    and (2 > self.velocity[1] > -2):
                if self.isBooster:
                    self.player.boost_active = True
                    self.player.bounce_value = 25
                    self.player.gravity /= 1.5
                self.player.velocity[1] = self.player.bounce_value

    def boost_platform(self):
        self.velocity[1] = self.player.platform_boost_velocity
        if self.velocity[1] < -40:
            self.player.boost_slowdown = True

    def move_platform(self):
        # update height of platforms
        if self.player.pos[1] >= 300 and not self.player.boost_active:
            # self.velocity[1] -= 2
            if self.player.velocity[1] > 0:
                if self.player.platform_velocity > -self.player.velocity[1]:
                    self.player.platform_velocity -= 0.4

            else:  # player is vertically decelerating
                if self.player.platform_velocity < 0:
                    self.player.platform_velocity += 0.1
            self.velocity[1] = self.player.platform_velocity

            # if self.velocity[1] < self.background_movement_speed:
            #     self.velocity[1] = -self.background_movement_speed
        else:
            # deceleration of platform when the player is not at the threshold until platform is stopped
            if self.velocity[1] < 0:
                self.velocity[1] += 1
            else:
                self.velocity[1] = 0