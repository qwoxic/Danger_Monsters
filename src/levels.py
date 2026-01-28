import random

class LevelManager:
    """Управление уровнями и их параметрами"""
    def __init__(self):
        self.current_level = 0
        self.enemies_killed = 0
        self.enemies_to_kill = 0
        self.spawn_timer = 0
        self.spawn_delay = 1.5
        self.max_enemies = 8
        
        # Конфигурация уровней
        self.level_configs = {
            1: {"enemies_to_kill": 5, "spawn_delay": 2.0, "enemy_speed": 60, "enemy_health": 30, "enemy_damage": 15},
            2: {"enemies_to_kill": 8, "spawn_delay": 1.8, "enemy_speed": 70, "enemy_health": 35, "enemy_damage": 18},
            3: {"enemies_to_kill": 10, "spawn_delay": 1.6, "enemy_speed": 80, "enemy_health": 40, "enemy_damage": 20},
            4: {"enemies_to_kill": 12, "spawn_delay": 1.4, "enemy_speed": 90, "enemy_health": 45, "enemy_damage": 22},
            5: {"enemies_to_kill": 0, "spawn_delay": 0, "enemy_speed": 100, "enemy_health": 50, "enemy_damage": 25}
        }
    
    def update(self, delta_time, enemy_list):
        """Обновление таймеров спавна"""
        self.spawn_timer += delta_time
        self._enemy_list = enemy_list
    
    def start_next_level(self, enemy_list):
        """Запуск следующего уровня"""
        self.current_level += 1
        self._enemy_list = enemy_list
        
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
        """Учет убитых врагов"""
        self.enemies_killed += 1
    
    def is_level_complete(self):
        """Проверка завершения уровня"""
        if self.current_level == 5:
            return False
        return self.enemies_killed >= self.enemies_to_kill
    
    def should_spawn_enemy(self):
        """Определение необходимости спавна врага"""
        if self.current_level == 5:
            return False
        if len(self._enemy_list) >= self.max_enemies:
            return False
        return self.spawn_timer >= self.spawn_delay
    
    def get_spawn_count(self):
        """Количество врагов для спавна"""
        self.spawn_timer = 0
        if self.current_level == 1:
            return 1
        elif self.current_level == 2:
            return random.randint(1, 2)
        else:
            return random.randint(1, 2)
    
    def get_enemy_speed(self):
        """Получение скорости врага для текущего уровня"""
        if self.current_level in self.level_configs:
            return self.level_configs[self.current_level]["enemy_speed"]
        return 60
    
    def get_enemy_health(self):
        """Получение здоровья врага для текущего уровня"""
        if self.current_level in self.level_configs:
            return self.level_configs[self.current_level]["enemy_health"]
        return 30
    
    def get_enemy_damage(self):
        """Получение урона врага для текущего уровня"""
        if self.current_level in self.level_configs:
            return self.level_configs[self.current_level]["enemy_damage"]
        return 15