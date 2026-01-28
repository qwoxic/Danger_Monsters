import arcade
import random
import math

class Boss(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(":resources:images/space_shooter/playerShip2_orange.png", scale=2.0)
        self.center_x = x
        self.center_y = y
        self.health = 400
        self.max_health = 400
        self.phase = 1
        self.attack_timer = 0
        self.spawn_timer = 0
        self.speed = 100
        self.rotation_angle = 0
        self.color = arcade.color.RED
        
    def update(self, delta_time, player, bullet_list, enemy_list, game_view):
        self.attack_timer += delta_time
        self.spawn_timer += delta_time
        
        if self.health < self.max_health * 0.3:
            self.phase = 3
            self.speed = 150
            self.color = arcade.color.MAGENTA
        elif self.health < self.max_health * 0.6:
            self.phase = 2
            self.speed = 120
            self.color = arcade.color.ORANGE_RED
        else:
            self.phase = 1
            self.speed = 100
            self.color = arcade.color.RED
        
        self.angle += delta_time * 20
        
        dx = player.center_x - self.center_x
        dy = player.center_y - self.center_y
        dist = max(math.sqrt(dx*dx + dy*dy), 1)
        
        if dist > 200:
            move_factor = 0.6 if self.phase == 1 else 0.9
            self.center_x += (dx / dist * self.speed * move_factor) * delta_time
            self.center_y += (dy / dist * self.speed * move_factor) * delta_time
        
        self.center_x = max(60, min(964, self.center_x))
        self.center_y = max(100, min(668, self.center_y))
        
        if self.attack_timer > 1.5:
            self.attack(player, bullet_list, game_view)
            self.attack_timer = 0
            
        if self.phase >= 2 and self.spawn_timer > 4:
            self.spawn_minions(enemy_list)
            self.spawn_timer = 0
    
    def attack(self, player, bullet_list, game_view):
        if game_view.shoot_sound:
            arcade.play_sound(game_view.shoot_sound, volume=0.3)
            
        if self.phase == 1:
            for angle in range(0, 360, 45):
                bullet = arcade.SpriteCircle(10, arcade.color.ORANGE)
                bullet.center_x = self.center_x
                bullet.center_y = self.center_y
                rad = math.radians(angle)
                bullet.change_x = math.cos(rad) * 200
                bullet.change_y = math.sin(rad) * 200
                bullet_list.append(bullet)
        
        elif self.phase == 2:
            for i in range(6):
                bullet = arcade.SpriteCircle(8, arcade.color.RED)
                bullet.center_x = self.center_x
                bullet.center_y = self.center_y
                dx = player.center_x - self.center_x
                dy = player.center_y - self.center_y
                dist = max(math.sqrt(dx*dx + dy*dy), 1)
                spread = (i - 3) * 0.15
                bullet.change_x = (dx / dist + spread) * 250
                bullet.change_y = (dy / dist + spread) * 250
                bullet_list.append(bullet)
        
        else:
            for i in range(10):
                bullet = arcade.SpriteCircle(6, arcade.color.CYAN)
                bullet.center_x = self.center_x
                bullet.center_y = self.center_y
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(180, 280)
                bullet.change_x = math.cos(angle) * speed
                bullet.change_y = math.sin(angle) * speed
                bullet_list.append(bullet)
            
            self.rotation_angle += 20
            for angle in range(0, 360, 30):
                bullet = arcade.SpriteCircle(7, arcade.color.MAGENTA)
                bullet.center_x = self.center_x
                bullet.center_y = self.center_y
                rad = math.radians(angle + self.rotation_angle)
                radius = 120
                bullet.change_x = math.cos(rad) * radius
                bullet.change_y = math.sin(rad) * radius
                bullet_list.append(bullet)
    
    def spawn_minions(self, enemy_list):
        from enemy import Enemy
        positions = []
        for _ in range(3):
            angle = random.uniform(0, 2 * math.pi)
            dist = random.uniform(80, 150)
            x = self.center_x + math.cos(angle) * dist
            y = self.center_y + math.sin(angle) * dist
            positions.append((x, y, angle))
        
        for x, y, angle in positions:
            minion = Enemy(x, y)
            minion.speed = 90
            minion.health = 30
            minion.scale = 0.5
            minion.color = arcade.color.GREEN
            minion.change_x = math.cos(angle) * 80
            minion.change_y = math.sin(angle) * 80
            enemy_list.append(minion)
    
    def take_damage(self, amount, game_view):
        self.health -= amount
        self.color = arcade.color.WHITE
        if game_view.hit_sound:
            arcade.play_sound(game_view.hit_sound, volume=0.3)
        if self.health <= 0:
            self.health = 0
        return self.health <= 0
