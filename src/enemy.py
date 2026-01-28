import arcade
import random
import math

class Enemy(arcade.Sprite):
    """Класс врага с базовым ИИ"""
    def __init__(self, x, y):
        super().__init__(":resources:images/space_shooter/playerShip1_orange.png", scale=0.5)
        self.center_x = x
        self.center_y = y
        self.speed = 60
        self.health = 30
        self.change_x = 0
        self.change_y = 0
        self.damage = 15
        self.invincible_timer = 0
        self.angle = 0

    def update(self, delta_time):
        """Обновление позиции и эффектов"""
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time
        
        self.angle += self.change_x * delta_time * 2
        
        # Эффект неуязвимости после получения урона
        if self.invincible_timer > 0:
            self.invincible_timer -= delta_time
            t = self.invincible_timer * 10
            self.color = (255, int(100 + 155 * abs(math.sin(t))), 100)
        else:
            self.color = (255, 255, 255)

    def move_towards(self, target_x, target_y, delta_time):
        """Движение к цели"""
        dx = target_x - self.center_x
        dy = target_y - self.center_y
        dist = max(math.sqrt(dx*dx + dy*dy), 1)
        
        self.change_x = dx / dist * self.speed
        self.change_y = dy / dist * self.speed
    
    def take_damage(self, amount):
        """Получение урона с таймером неуязвимости"""
        if self.invincible_timer <= 0:
            self.health -= amount
            self.invincible_timer = 0.3
            if self.health <= 0:
                self.health = 0
        return self.health <= 0
    
    def attack_player(self, player):
        """Атака игрока с отталкиванием"""
        if self.invincible_timer <= 0:
            player.take_damage(self.damage)
            self.invincible_timer = 0.5
            
            # Отталкивание при атаке
            dx = self.center_x - player.center_x
            dy = self.center_y - player.center_y
            dist = max(math.sqrt(dx*dx + dy*dy), 1)
            push_force = 120
            self.change_x += dx / dist * push_force
            self.change_y += dy / dist * push_force
            
            return True
        return False