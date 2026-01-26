import random

class LevelManager:
    def __init__(self):
        self.current_level = 0
        self.enemies_killed = 0
        self.enemies_to_kill = 0
        self.spawn_timer = 0
        self.spawn_delay = 1.5
        self.max_enemies = 10
        
        # Уменьшил количество врагов для более быстрого прохождения
        self.level_configs = {
            1: {"enemies_to_kill": 5, "spawn_delay": 2.0, "enemy_speed": 60, "enemy_health": 60},
            2: {"enemies_to_kill": 8, "spawn_delay": 1.8, "enemy_speed": 70, "enemy_health": 70},
            3: {"enemies_to_kill": 10, "spawn_delay": 1.6, "enemy_speed": 80, "enemy_health": 80},
            4: {"enemies_to_kill": 12, "spawn_delay": 1.4, "enemy_speed": 90, "enemy_health": 90},
            5: {"enemies_to_kill": 0, "spawn_delay": 0, "enemy_speed": 100, "enemy_health": 100}
        }
    
    def update(self, delta_time):
        self.spawn_timer += delta_time
    
    def start_next_level(self):
        self.current_level += 1
        
        if self.current_level > 5:
            return "complete"
        
        if self.current_level == 5:
            self.enemies_to_kill = 0
            return "boss"
        
        config = self.level_configs[self.current_level]
        self.enemies_to_kill = config["enemies_to_kill"]
        self.spawn_delay = config["spawn_delay"]
        self.enemies_killed = 0
        return "normal"
    
    def enemy_killed(self):
        self.enemies_killed += 1
    
    def is_level_complete(self):
        if self.current_level == 5:
            return False
        return self.enemies_killed >= self.enemies_to_kill
    
    def should_spawn_enemy(self):
        if self.current_level == 5:
            return False
        if len(self.enemy_list) >= self.max_enemies:  # Ограничиваем максимальное количество врагов
            return False
        return self.spawn_timer >= self.spawn_delay
    
    def get_spawn_count(self):
        self.spawn_timer = 0
        if self.current_level == 1:
            return 1
        elif self.current_level == 2:
            return random.randint(1, 2)
        else:
            return random.randint(1, 2)  # Уменьшил спавн
    
    def get_enemy_speed(self):
        if self.current_level in self.level_configs:
            return self.level_configs[self.current_level]["enemy_speed"]
        return 60
    
    def get_enemy_health(self):
        if self.current_level in self.level_configs:
            return self.level_configs[self.current_level]["enemy_health"]
        return 60
    
    @property
    def enemy_list(self):
        # Это свойство нужно для проверки количества врагов
        # В реальной игре этот метод должен возвращать ссылку на список врагов
        return []