# skills/file_manager_skill.py
import os
from skills.base_skill import BaseSkill

class FileManagerSkill(BaseSkill):
    def handle(self, text, player):
        text_lower = text.lower()
        try:
            if "open folder" in text_lower:
                folder = text_lower.split("open folder")[1].strip()
                path = os.path.expanduser(f"~/Desktop/{folder}")
                os.startfile(path)
                return True, f"Opened folder {folder}"
            elif "create folder" in text_lower:
                folder = text_lower.split("create folder")[1].strip()
                path = os.path.expanduser(f"~/Desktop/{folder}")
                os.makedirs(path, exist_ok=True)
                return True, f"Created folder {folder}"
        except Exception as e:
            return True, f"Error: {e}"
        return False, None
