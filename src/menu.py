import arcade
from database import save_score, get_high_scores

class MenuView(arcade.View):
    """Главное меню с таблицей рекордов"""
    def on_draw(self):
        """Отрисовка меню"""
        self.clear()
        arcade.set_background_color((10, 10, 20))
        
        # Заголовок и инструкции
        arcade.draw_text("DANGER MONSTERS", 512, 600, 
                         arcade.color.CYAN, 48, anchor_x="center")
        arcade.draw_text("ЛКМ или ENTER - начать", 512, 450, 
                         arcade.color.LIGHT_GRAY, 24, anchor_x="center")
        arcade.draw_text("ESC в игре - выйти в меню", 512, 400, 
                         arcade.color.LIGHT_GRAY, 20, anchor_x="center")
        arcade.draw_text("Таблица результатов:", 512, 300, 
                         arcade.color.YELLOW, 22, anchor_x="center")
        
        # Таблица рекордов
        scores = get_high_scores(5)
        y_pos = 250
        for i, (name, score, date) in enumerate(scores):
            arcade.draw_text(f"{i+1}. {name}: {score} очков ({date[:10]})", 
                           512, y_pos, arcade.color.LIGHT_GRAY, 18, anchor_x="center")
            y_pos -= 30
        
        arcade.draw_text("Нажмите Q для выхода", 512, 100, 
                         arcade.color.LIGHT_GRAY, 20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        """Обработка клавиш в меню"""
        if key == arcade.key.ENTER:
            from game import GameView
            self.window.show_view(GameView())
        elif key == arcade.key.Q:
            self.window.close()

    def on_mouse_press(self, x, y, button, modifiers):
        """Запуск игры по клику"""
        from game import GameView
        self.window.show_view(GameView())

class GameOverView(arcade.View):
    """Экран завершения игры (победа/поражение)"""
    def __init__(self, score, won):
        super().__init__()
        self.score = score
        self.won = won
        save_score("Игрок", score)
    
    def on_draw(self):
        """Отрисовка экрана завершения"""
        self.clear()
        arcade.set_background_color((15, 15, 25))
        
        if self.won:
            title = "ПОБЕДА!"
            color = arcade.color.GREEN
            message = "Вы победили Босса!"
        else:
            title = "ПОРАЖЕНИЕ"
            color = arcade.color.RED
            message = "Вы погибли"
        
        arcade.draw_text(title, 512, 500, color, 48, anchor_x="center")
        arcade.draw_text(message, 512, 430, arcade.color.WHITE, 32, anchor_x="center")
        arcade.draw_text(f"Очки: {self.score}", 512, 350, 
                         arcade.color.YELLOW, 36, anchor_x="center")
        arcade.draw_text("Нажмите ENTER для возврата в меню", 512, 250, 
                         arcade.color.LIGHT_GRAY, 24, anchor_x="center")
        arcade.draw_text("Нажмите Q для выхода", 512, 200, 
                         arcade.color.LIGHT_GRAY, 20, anchor_x="center")
    
    def on_key_press(self, key, modifiers):
        """Обработка клавиш на экране завершения"""
        if key == arcade.key.ENTER:
            self.window.show_view(MenuView())
        elif key == arcade.key.Q:
            self.window.close()