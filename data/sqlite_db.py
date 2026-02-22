import sqlite3
from pathlib import Path

DB_PATH = Path("memory/moon.db")

class MoonDB:
    def __init__(self):
        DB_PATH.parent.mkdir(exist_ok=True)
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

    # ---------- PROFILE ----------
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

    # ---------- CONVERSATIONS ----------
    def log_conversation(self, user, assistant, intent="unknown"):
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO conversations(user_text,assistant_text,intent)
        VALUES(?,?,?)
        """, (user, assistant, intent))
        self.conn.commit()

    def get_recent_conversations(self, limit=5):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT user_text, assistant_text FROM conversations
        ORDER BY id DESC LIMIT ?
        """, (limit,))
        return cursor.fetchall()

    # ---------- TASKS ----------
    def add_task(self, title, due=None):
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO tasks(title,status,due_date)
        VALUES(?,?,?)
        """, (title, "pending", due))
        self.conn.commit()

    def get_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id,title,status FROM tasks")
        return cursor.fetchall()

    def complete_task(self, task_id):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE tasks SET status='done' WHERE id=?", (task_id,))
        self.conn.commit()