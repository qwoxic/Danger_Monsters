import sqlite3
import datetime

def init_database():
    """Инициализация базы данных для хранения рекордов"""
    conn = sqlite3.connect('game_scores.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scores
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  player_name TEXT NOT NULL,
                  score INTEGER NOT NULL,
                  date TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def save_score(player_name, score):
    """Сохранение результата в базу данных"""
    init_database()
    conn = sqlite3.connect('game_scores.db')
    c = conn.cursor()
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO scores (player_name, score, date) VALUES (?, ?, ?)",
              (player_name, score, date))
    conn.commit()
    conn.close()

def get_high_scores(limit=10):
    """Получение таблицы рекордов"""
    init_database()
    conn = sqlite3.connect('game_scores.db')
    c = conn.cursor()
    c.execute("SELECT player_name, score, date FROM scores ORDER BY score DESC LIMIT ?", (limit,))
    scores = c.fetchall()
    conn.close()
    return scores