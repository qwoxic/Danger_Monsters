import arcade
import math

class Player(arcade.Sprite):
    """Класс игрока с управлением и здоровьем"""
    def __init__(self, x, y):
        super().__init__(":resources:images/space_shooter/playerShip1_blue.png", scale=0.7)
        self.center_x = x
        self.center_y = y
        self.health = 100
        self.max_health = 100
        self.change_x = 0
        self.change_y = 0
        self.invincible_timer = 0
        self.angle = 0

    def update(self, delta_time):
        """Обновление позиции и состояния"""
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time
        
        # Поворот корабля в сторону движения
        if self.change_x != 0 or self.change_y != 0:
            self.angle = math.degrees(math.atan2(-self.change_x, self.change_y))
        
        # Ограничение движения границами экрана
        self.center_x = max(40, min(1004, self.center_x))
        self.center_y = max(40, min(748, self.center_y))
        
        # Эффект неуязвимости после получения урона
        if self.invincible_timer > 0:
            self.invincible_timer -= delta_time
            t = self.invincible_timer * 8
            self.alpha = int(150 + 105 * abs(math.sin(t)))
        else:
            self.alpha = 255

    def take_damage(self, amount):
        """Получение урона игроком"""
        if self.invincible_timer <= 0:
            self.health -= amount
            self.invincible_timer = 0.8
            if self.health <= 0:
                self.health = 0
                self.alpha = 100
            return self.health <= 0
        return False