import arcade
import random
import math

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        
        self.player = arcade.SpriteCircle(20, arcade.color.BLUE)
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.player.health = 100
        self.player.change_x = 0
        self.player.change_y = 0
        
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
        
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        
        self.score = 0
        self.spawn_timer = 0.0
        self.spawn_interval = 2.0
        
        for _ in range(3):
            self.spawn_enemy()

    def on_draw(self):
        self.clear()
        
        self.player_list.draw()
        self.enemy_list.draw()
        self.bullet_list.draw()
        
        arcade.draw_text(f"Score: {self.score}", 20, SCREEN_HEIGHT - 40, 
                         arcade.color.WHITE, 24)
        arcade.draw_text(f"HP: {self.player.health}", 
                         20, SCREEN_HEIGHT - 80, arcade.color.WHITE, 24)

    def on_update(self, delta_time):
        self.spawn_timer += delta_time
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0.0
            self.spawn_enemy()
        
        self.player.center_x += self.player.change_x * delta_time
        self.player.center_y += self.player.change_y * delta_time
        
        self.player.center_x = max(20, min(SCREEN_WIDTH - 20, self.player.center_x))
        self.player.center_y = max(20, min(SCREEN_HEIGHT - 20, self.player.center_y))
        
        for enemy in self.enemy_list:
            dx = self.player.center_x - enemy.center_x
            dy = self.player.center_y - enemy.center_y
            dist = max(math.sqrt(dx*dx + dy*dy), 1)
            
            enemy.center_x += dx / dist * enemy.speed * delta_time
            enemy.center_y += dy / dist * enemy.speed * delta_time
        
        for bullet in self.bullet_list:
            bullet.center_x += bullet.change_x * delta_time
            bullet.center_y += bullet.change_y * delta_time
            
            if (bullet.center_x < -100 or bullet.center_x > SCREEN_WIDTH + 100 or 
                bullet.center_y < -100 or bullet.center_y > SCREEN_HEIGHT + 100):
                bullet.remove_from_sprite_lists()
        
        hits = arcade.check_for_collision_with_list(self.player, self.enemy_list)
        for enemy in hits:
            enemy.remove_from_sprite_lists()
            self.player.health -= 20
            if self.player.health <= 0:
                self.respawn_player()
        
        for bullet in self.bullet_list[:]:
            hit_enemies = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            if hit_enemies:
                for enemy in hit_enemies:
                    enemy.health -= 25
                    if enemy.health <= 0:
                        enemy.remove_from_sprite_lists()
                        self.score += 50
                bullet.remove_from_sprite_lists()

    def respawn_player(self):
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.player.health = 100
        
        self.enemy_list.clear()
        self.bullet_list.clear()
        
        for _ in range(3):
            self.spawn_enemy()

    def spawn_enemy(self):
        if len(self.enemy_list) >= 10:
            return
            
        side = random.choice(['top', 'bottom', 'left', 'right'])
        
        if side == 'top':
            x = random.randint(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT + 20
        elif side == 'bottom':
            x = random.randint(0, SCREEN_WIDTH)
            y = -20
        elif side == 'left':
            x = -20
            y = random.randint(0, SCREEN_HEIGHT)
        else:
            x = SCREEN_WIDTH + 20
            y = random.randint(0, SCREEN_HEIGHT)
        
        enemy = arcade.SpriteCircle(15, arcade.color.RED)
        enemy.center_x = x
        enemy.center_y = y
        enemy.speed = random.randint(60, 100)
        enemy.health = 60
        
        self.enemy_list.append(enemy)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player.change_y = 300
        elif key == arcade.key.S:
            self.player.change_y = -300
        elif key == arcade.key.A:
            self.player.change_x = -300
        elif key == arcade.key.D:
            self.player.change_x = 300
        elif key == arcade.key.ESCAPE:
            from menu import MenuView
            self.window.show_view(MenuView())

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.S):
            self.player.change_y = 0
        if key in (arcade.key.A, arcade.key.D):
            self.player.change_x = 0

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            dx = x - self.player.center_x
            dy = y - self.player.center_y
            dist = max(math.sqrt(dx*dx + dy*dy), 1)
            
            bullet = arcade.SpriteCircle(5, arcade.color.YELLOW)
            bullet.center_x = self.player.center_x
            bullet.center_y = self.player.center_y
            bullet.change_x = dx / dist * 500
            bullet.change_y = dy / dist * 500
            
            self.bullet_list.append(bullet)
