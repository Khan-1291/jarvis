import sqlite3
from pathlib import Path

DB_PATH = Path("memory/moon.db")

class MoonDB:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profile(
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_text TEXT,
            assistant_text TEXT,
            intent TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            status TEXT,
            due_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.conn.commit()

    def set_profile(self, key, value):
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO user_profile(key,value)
        VALUES(?,?)
        ON CONFLICT(key) DO UPDATE SET value=excluded.value
        """, (key,value))
        self.conn.commit()

    def get_profile(self, key):
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM user_profile WHERE key=?", (key,))
        row = cursor.fetchone()
        return row[0] if row else None