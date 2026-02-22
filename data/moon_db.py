def get_recent_conversations(self, limit=6):
    cursor = self.conn.cursor()
    cursor.execute("""
        SELECT user, assistant
        FROM conversations
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    return cursor.fetchall()