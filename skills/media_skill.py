# skills/media_skill.py
import pyautogui
from skills.base_skill import BaseSkill

class MediaSkill(BaseSkill):
    def handle(self, text, player):
        text_lower = text.lower()
        try:
            if "play music" in text_lower:
                pyautogui.press("playpause")
                return True, "Toggled play/pause"
            elif "next song" in text_lower:
                pyautogui.press("nexttrack")
                return True, "Skipping song"
        except Exception as e:
            return True, f"Error: {e}"
        return False, None
