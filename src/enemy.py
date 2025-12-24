import arcade
import random
import math

class Enemy(arcade.SpriteCircle):
    def __init__(self, x, y):
        super().__init__(15, arcade.color.RED)
        self.center_x = x
        self.center_y = y
        self.speed = random.randint(50, 80)
        self.health = 60
        self.change_x = 0
        self.change_y = 0

    def update(self, delta_time):
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

    def move_towards(self, target_x, target_y, delta_time):
        dx = target_x - self.center_x
        dy = target_y - self.center_y
        dist = max(math.sqrt(dx*dx + dy*dy), 1)
        
        self.change_x = dx / dist * self.speed
        self.change_y = dy / dist * self.speed
