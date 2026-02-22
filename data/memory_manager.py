from memory.sqlite_db import MoonDB

class MemoryManager:
    def __init__(self):
        self.db = MoonDB()

    # ---------- PROFILE ----------
    def remember_name(self, name):
        self.db.set_profile("name", name)

    def recall_name(self):
        return self.db.get_profile("name")

    # ---------- TASKS ----------
    def add_task(self, title):
        self.db.add_task(title)

    def list_tasks(self):
        return self.db.get_tasks()

    # ---------- CONVERSATION ----------
    def save_interaction(self, user, assistant, intent="unknown"):
        self.db.log_conversation(user, assistant, intent)

    def get_context(self):
        rows = self.db.get_recent_conversations()
        context = ""
        for u,a in rows[::-1]:
            context += f"User: {u}\nAssistant: {a}\n"
        return context