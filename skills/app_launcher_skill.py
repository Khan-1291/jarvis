# skills/app_launcher_skill.py
import subprocess
import psutil
from skills.base_skill import BaseSkill

class AppLauncherSkill(BaseSkill):
    apps = {
        "chrome": "chrome",
        "vs code": "code",
        "notepad": "notepad"
    }

    def handle(self, text, player):
        text_lower = text.lower()
        try:
            for app_name, cmd in self.apps.items():
                if f"open {app_name}" in text_lower:
                    subprocess.Popen(cmd)
                    return True, f"Opening {app_name}"
                elif f"close {app_name}" in text_lower:
                    for proc in psutil.process_iter(['name']):
                        if app_name in proc.info['name'].lower():
                            proc.kill()
                    return True, f"Closed {app_name}"
        except Exception as e:
            return True, f"Error: {e}"
        return False, None
