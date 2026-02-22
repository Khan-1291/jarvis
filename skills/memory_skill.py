# skills/memory_skill.py
from skills.base_skill import BaseSkill

class MemorySkill(BaseSkill):
    def __init__(self, memory):
        self.memory = memory

    def handle(self, text, player):
        text_lower = text.lower()

        # Remember a fact
        if "remember that" in text_lower:
            parts = text_lower.split("remember that")[1].strip().split(" is ", 1)
            if len(parts) == 2:
                key, value = parts
                self.memory.remember(key.strip(), value.strip())
                return True, f"I will remember that {key.strip()} is {value.strip()}"
            return True, "Sorry, I couldn't understand what to remember."

        # Recall a fact
        elif "what is" in text_lower:
            key = text_lower.split("what is")[1].strip()
            value = self.memory.recall(key)
            if value:
                return True, f"{key} is {value}"
            else:
                return True, f"I don't remember anything about {key}"

        # Forget a fact
        elif "forget" in text_lower:
            key = text_lower.split("forget")[1].strip()
            self.memory.forget(key)
            return True, f"I forgot about {key}"

        # List all persistent memories
        elif "list memories" in text_lower:
            mems = self.memory.list_memory()
            if mems:
                return True, "Here is what I remember: " + ", ".join([f"{k}: {v}" for k, v in mems.items()])
            else:
                return True, "I don't remember anything yet."

        # Contextual session queries
        elif "what did i say" in text_lower:
            context = self.memory.get_context()
            if context:
                last_user = context[-1]["user"]
                return True, f"The last thing you said was: '{last_user}'"
            return True, "You haven't said anything yet."

        return False, None
