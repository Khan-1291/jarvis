# memory/memory.py
import sqlite3
import json
from datetime import datetime
from typing import Dict, Any, List, Optional, Union

class Memory:
    def __init__(self, db_path: str = "moon_memory.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(
            self.db_path,
            check_same_thread=False,     # ← Critical fix for threading issue
            timeout=15.0
        )
        # Better concurrency & performance
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
        print(f"Memory initialized → {self.db_path}")

    def _create_tables(self):
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS facts (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                type TEXT DEFAULT 'text'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_text TEXT NOT NULL,
                assistant_text TEXT NOT NULL,
                context_summary TEXT
            )
        ''')
        
        self.conn.commit()

    # ────────────────────────────────────────────────
    #  Fact Management
    # ────────────────────────────────────────────────

    def remember(self, key: str, value: Any, type_hint: str = None):
        cursor = self.conn.cursor()

        if isinstance(value, (list, dict)):
            stored_value = json.dumps(value, ensure_ascii=False)
            fact_type = type_hint or 'json'
        elif isinstance(value, bool):
            stored_value = json.dumps(value)
            fact_type = 'bool'
        else:
            stored_value = str(value)
            fact_type = type_hint or 'text'

        # Append-style keys
        append_keys = {'likes', 'dislikes', 'hobbies', 'goals', 'avoid', 'favorite_movies'}
        if key in append_keys and self.has_fact(key):
            current = self.get(key, default=[])
            if isinstance(current, list) and value not in current:
                current.append(value)
                stored_value = json.dumps(current)
                fact_type = 'list'

        now = datetime.utcnow().isoformat()
        cursor.execute('''
            INSERT OR REPLACE INTO facts (key, value, updated_at, type)
            VALUES (?, ?, ?, ?)
        ''', (key, stored_value, now, fact_type))

        self.conn.commit()
        print(f"→ Remembered: {key} = {value}")

    def forget(self, key: str):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM facts WHERE key = ?", (key,))
        self.conn.commit()
        print(f"→ Forgot: {key}")

    def get(self, key: str, default: Any = None) -> Any:
        cursor = self.conn.cursor()
        cursor.execute("SELECT value, type FROM facts WHERE key = ?", (key,))
        row = cursor.fetchone()
        if not row:
            return default

        value_str, typ = row['value'], row['type']

        if typ in ('json', 'list'):
            try:
                return json.loads(value_str)
            except:
                return value_str
        elif typ == 'bool':
            return value_str.lower() in ('true', '1', 'yes', 'on')
        else:
            return value_str

    def has_fact(self, key: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("SELECT 1 FROM facts WHERE key = ?", (key,))
        return cursor.fetchone() is not None

    def get_all_facts(self) -> Dict[str, Any]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT key, value, type FROM facts ORDER BY updated_at DESC")
        result = {}
        for row in cursor.fetchall():
            val = row['value']
            if row['type'] in ('json', 'list'):
                try:
                    result[row['key']] = json.loads(val)
                except:
                    result[row['key']] = val
            else:
                result[row['key']] = val
        return result

    # ────────────────────────────────────────────────
    #  Conversation History
    # ────────────────────────────────────────────────

    def add_conversation(self, user_text: str, assistant_text: str, summary: str = None):
        cursor = self.conn.cursor()
        now = datetime.utcnow().isoformat()
        cursor.execute('''
            INSERT INTO conversations (timestamp, user_text, assistant_text, context_summary)
            VALUES (?, ?, ?, ?)
        ''', (now, user_text, assistant_text, summary))
        self.conn.commit()

    def get_recent_conversations(self, limit: int = 8) -> List[Dict]:
        """Returns list of dicts: [{'timestamp':..., 'user':..., 'assistant':..., 'summary':...}]"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT timestamp, user_text, assistant_text, context_summary
            FROM conversations
            ORDER BY id DESC
            LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        return [
            {
                "timestamp": r["timestamp"],
                "user": r["user_text"],
                "assistant": r["assistant_text"],
                "summary": r["context_summary"]
            }
            for r in reversed(rows)  # oldest → newest
        ]

    def get_conversation_count(self) -> int:
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM conversations")
        return cursor.fetchone()[0]

    def close(self):
        if self.conn:
            self.conn.close()

    def __del__(self):
        self.close()