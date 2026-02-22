# skills/system_control_skill.py
import os
import pyautogui
from skills.base_skill import BaseSkill

class SystemControlSkill(BaseSkill):
    def handle(self, text, player):
        text_lower = text.lower()
        try:
            if "shutdown" in text_lower:
                os.system("shutdown /s /t 10")
                return True, "Shutting down in 1 minute"
            elif "restart" in text_lower:
                os.system("shutdown /r /t 60")
                return True, "Restarting in 1 minute"
            elif "volume up" in text_lower:
                pyautogui.press("volumeup")
                return True, "Volume increased"
            elif "volume down" in text_lower:
                pyautogui.press("volumedown")
                return True, "Volume decreased"
        except Exception as e:
            return True, f"Error: {e}"
        return False, None
