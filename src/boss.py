import arcade
import random
import math

class Boss(arcade.SpriteCircle):
    def __init__(self, x, y):
        super().__init__(40, arcade.color.PURPLE)
        self.center_x = x
        self.center_y = y
        self.health = 500
        self.max_health = 500
        self.phase = 1
        self.attack_timer = 0
        self.spawn_timer = 0
        self.speed = 100
        
    def update(self, delta_time, player, bullet_list):
        self.attack_timer += delta_time
        self.spawn_timer += delta_time
        
        # Определяем фазу босса
        if self.health < self.max_health * 0.3:
            self.phase = 3
            self.speed = 150
        elif self.health < self.max_health * 0.6:
            self.phase = 2
            self.speed = 120
        else:
            self.phase = 1
            self.speed = 100
        
        # Движение к игроку
        dx = player.center_x - self.center_x
        dy = player.center_y - self.center_y
        dist = max(math.sqrt(dx*dx + dy*dy), 1)
        
        move_factor = 0.5 if self.phase == 1 else 0.8
        self.center_x += (dx / dist * self.speed * move_factor) * delta_time
        self.center_y += (dy / dist * self.speed * move_factor) * delta_time
        
        # Ограничение движения по экрану
        self.center_x = max(40, min(984, self.center_x))
        self.center_y = max(40, min(728, self.center_y))
        
        # Атаки
        if self.attack_timer > 1.5:
            self.attack(player, bullet_list)
            self.attack_timer = 0
            
        if self.phase >= 2 and self.spawn_timer > 3:
            self.spawn_minions(bullet_list)
            self.spawn_timer = 0
    
    def attack(self, player, bullet_list):
        if self.phase == 1:
            # Круговые атаки
            for angle in range(0, 360, 45):
                bullet = arcade.SpriteCircle(8, arcade.color.ORANGE)
                bullet.center_x = self.center_x
                bullet.center_y = self.center_y
                rad = math.radians(angle)
                bullet.change_x = math.cos(rad) * 200
                bullet.change_y = math.sin(rad) * 200
                bullet_list.append(bullet)
        
        elif self.phase == 2:
            # Прицельные атаки с разбросом
            for i in range(5):
                bullet = arcade.SpriteCircle(6, arcade.color.RED)
                bullet.center_x = self.center_x
                bullet.center_y = self.center_y
                dx = player.center_x - self.center_x
                dy = player.center_y - self.center_y
                dist = max(math.sqrt(dx*dx + dy*dy), 1)
                spread = (i - 2) * 0.2
                bullet.change_x = (dx / dist + spread) * 250
                bullet.change_y = (dy / dist + spread) * 250
                bullet_list.append(bullet)
        
        else:
            # Хаотичные атаки
            for i in range(8):
                bullet = arcade.SpriteCircle(4, arcade.color.CYAN)
                bullet.center_x = self.center_x
                bullet.center_y = self.center_y
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(150, 250)
                bullet.change_x = math.cos(angle) * speed
                bullet.change_y = math.sin(angle) * speed
                bullet_list.append(bullet)
    
    def spawn_minions(self, bullet_list):
        # Призыв миньонов (упрощенный - просто пули-миньоны)
        for _ in range(2):
            minion = arcade.SpriteCircle(10, arcade.color.DARK_GREEN)
            angle = random.uniform(0, 2 * math.pi)
            dist = 50
            minion.center_x = self.center_x + math.cos(angle) * dist
            minion.center_y = self.center_y + math.sin(angle) * dist
            minion.change_x = math.cos(angle) * 100
            minion.change_y = math.sin(angle) * 100
            minion.health = 30
            bullet_list.append(minion)
    
    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0