import arcade
import random
import math
from levels import LevelManager
from player import Player
from enemy import Enemy
from boss import Boss

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        
        self.level_manager = LevelManager()
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
        
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.boss_bullet_list = arcade.SpriteList()
        self.boss_list = arcade.SpriteList()
        self.particles = arcade.SpriteList()
        
        self.stars = []
        for _ in range(150):
            self.stars.append((
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
                random.uniform(0.5, 1.5),
                random.randint(100, 255)
            ))
        
        self.score = 0
        self.is_boss_level = False
        self.boss = None
        
        try:
            self.shoot_sound = arcade.load_sound(":resources:sounds/laser2.wav")
            self.hit_sound = arcade.load_sound(":resources:sounds/hit3.wav")
            self.explosion_sound = arcade.load_sound(":resources:sounds/explosion2.wav")
            self.boss_shoot_sound = arcade.load_sound(":resources:sounds/laser1.wav")
        except:
            self.shoot_sound = None
            self.hit_sound = None
            self.explosion_sound = None
            self.boss_shoot_sound = None
        
        self.level_type = self.level_manager.start_next_level(self.enemy_list)
        if self.level_type == "boss":
            self.start_boss_level()

    def on_draw(self):
        self.clear()
        
        arcade.set_background_color((5, 5, 20))
        
        for x, y, size, brightness in self.stars:
            color = (brightness, brightness, brightness)
            arcade.draw_circle_filled(x, y, size, color)
        
        self.player_list.draw()
        self.enemy_list.draw()
        self.bullet_list.draw()
        self.boss_bullet_list.draw()
        self.boss_list.draw()
        self.particles.draw()
        
        arcade.draw_text(f"Уровень: {self.level_manager.current_level}", 20, SCREEN_HEIGHT - 40, 
                         arcade.color.WHITE, 24)
        arcade.draw_text(f"Очки: {self.score}", 20, SCREEN_HEIGHT - 80, 
                         arcade.color.WHITE, 24)
        
        hp_color = arcade.color.GREEN
        if self.player.health < 30:
            hp_color = arcade.color.RED
        elif self.player.health < 60:
            hp_color = arcade.color.YELLOW
        
        arcade.draw_text(f"HP: {self.player.health}", 
                         20, SCREEN_HEIGHT - 120, hp_color, 24)
        
        if self.is_boss_level and self.boss:
            boss_hp_color = arcade.color.RED
            if self.boss.health > 200:
                boss_hp_color = arcade.color.GREEN
            elif self.boss.health > 100:
                boss_hp_color = arcade.color.YELLOW
            
            arcade.draw_text(f"Босс HP: {self.boss.health}", 
                             SCREEN_WIDTH - 200, SCREEN_HEIGHT - 40, 
                             boss_hp_color, 24)

    def on_update(self, delta_time):
        self.level_manager.update(delta_time, self.enemy_list)
        
        if self.is_boss_level:
            if not self.boss or self.boss.health <= 0:
                self.score += 1000
                self.level_type = self.level_manager.start_next_level(self.enemy_list)
                if self.level_type == "complete":
                    self.win_game()
                    return
                elif self.level_type == "boss":
                    self.start_boss_level()
                else:
                    self.is_boss_level = False
                    self.boss = None
                    self.boss_list.clear()
                return
            self.boss.update(delta_time, self.player, self.boss_bullet_list, self.enemy_list, self)
        else:
            self.spawn_enemies()
        
        self.player.update(delta_time)
        
        for enemy in self.enemy_list:
            enemy.update(delta_time)
            enemy.move_towards(self.player.center_x, self.player.center_y, delta_time)
        
        for bullet in self.bullet_list:
            bullet.center_x += bullet.change_x * delta_time
            bullet.center_y += bullet.change_y * delta_time
            if (bullet.center_x < -100 or bullet.center_x > SCREEN_WIDTH + 100 or 
                bullet.center_y < -100 or bullet.center_y > SCREEN_HEIGHT + 100):
                bullet.remove_from_sprite_lists()
        
        for bullet in self.boss_bullet_list:
            bullet.center_x += bullet.change_x * delta_time
            bullet.center_y += bullet.change_y * delta_time
            if (bullet.center_x < -100 or bullet.center_x > SCREEN_WIDTH + 100 or 
                bullet.center_y < -100 or bullet.center_y > SCREEN_HEIGHT + 100):
                bullet.remove_from_sprite_lists()
        
        for particle in self.particles:
            particle.center_x += particle.change_x * delta_time
            particle.center_y += particle.change_y * delta_time
            particle.lifetime -= delta_time
            particle.alpha = int(255 * (particle.lifetime / 0.5))
            if particle.lifetime <= 0:
                particle.remove_from_sprite_lists()
        
        for enemy in self.enemy_list[:]:
            if arcade.check_for_collision(enemy, self.player):
                if enemy.attack_player(self.player):
                    if self.hit_sound:
                        arcade.play_sound(self.hit_sound, volume=0.3)
                    if self.player.health <= 0:
                        self.game_over()
                        return
        
        for bullet in self.boss_bullet_list[:]:
            if arcade.check_for_collision(bullet, self.player):
                if self.player.take_damage(15):
                    if self.hit_sound:
                        arcade.play_sound(self.hit_sound, volume=0.3)
                    self.game_over()
                bullet.remove_from_sprite_lists()
        
        for bullet in self.bullet_list[:]:
            hit_enemies = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            if hit_enemies:
                for enemy in hit_enemies:
                    if enemy.take_damage(25):
                        self.create_death_particles(enemy.center_x, enemy.center_y)
                        if self.explosion_sound:
                            arcade.play_sound(self.explosion_sound, volume=0.2)
                        enemy.remove_from_sprite_lists()
                        self.score += 50
                        self.level_manager.enemy_killed()
                bullet.remove_from_sprite_lists()
            
            if self.boss and arcade.check_for_collision(bullet, self.boss):
                if self.boss.take_damage(25, self):
                    if self.explosion_sound:
                        arcade.play_sound(self.explosion_sound, volume=0.5)
                    self.boss.remove_from_sprite_lists()
                bullet.remove_from_sprite_lists()
        
        if not self.is_boss_level and self.level_manager.is_level_complete():
            self.level_type = self.level_manager.start_next_level(self.enemy_list)
            if self.level_type == "boss":
                self.start_boss_level()
            else:
                self.enemy_list.clear()
                self.bullet_list.clear()

    def create_death_particles(self, x, y):
        colors = [arcade.color.ORANGE, arcade.color.YELLOW, arcade.color.RED]
        for _ in range(12):
            particle = arcade.SpriteCircle(4, random.choice(colors))
            particle.center_x = x
            particle.center_y = y
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(80, 200)
            particle.change_x = math.cos(angle) * speed
            particle.change_y = math.sin(angle) * speed
            particle.lifetime = 0.5
            self.particles.append(particle)

    def spawn_enemies(self):
        if self.level_manager.should_spawn_enemy():
            for _ in range(self.level_manager.get_spawn_count()):
                self.spawn_enemy()

    def spawn_enemy(self):
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
        
        enemy = Enemy(x, y)
        enemy.speed = self.level_manager.get_enemy_speed()
        enemy.health = self.level_manager.get_enemy_health()
        enemy.damage = self.level_manager.get_enemy_damage()
        self.enemy_list.append(enemy)

    def game_over(self):
        from menu import GameOverView
        self.window.show_view(GameOverView(self.score, False))

    def win_game(self):
        from menu import GameOverView
        self.window.show_view(GameOverView(self.score, True))

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player.change_y = 300
        elif key == arcade.key.S:
            self.player.change_y = -300
        elif key == arcade.key.A:
            self.player.change_x = -300
        elif key == arcade.key.D:
            self.player.change_x = 300
        elif key == arcade.key.SPACE:
            self.shoot_at_mouse()
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
            self.shoot_at_position(x, y)

    def shoot_at_position(self, x, y):
        dx = x - self.player.center_x
        dy = y - self.player.center_y
        dist = max(math.sqrt(dx*dx + dy*dy), 1)
        
        bullet = arcade.SpriteCircle(6, arcade.color.YELLOW)
        bullet.center_x = self.player.center_x
        bullet.center_y = self.player.center_y
        bullet.change_x = dx / dist * 500
        bullet.change_y = dy / dist * 500
        
        self.bullet_list.append(bullet)
        
        if self.shoot_sound:
            arcade.play_sound(self.shoot_sound, volume=0.2)

    def shoot_at_mouse(self):
        mouse_x = arcade.get_mouse_x()
        mouse_y = arcade.get_mouse_y()
        self.shoot_at_position(mouse_x, mouse_y)

    def start_boss_level(self):
        self.is_boss_level = True
        self.enemy_list.clear()
        self.bullet_list.clear()
        self.boss = Boss(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
        self.boss_list.clear()
        self.boss_list.append(self.boss)