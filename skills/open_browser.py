# skills/open_browser.py
from .base_skill import BaseSkill
import webbrowser
from datetime import datetime

class OpenBrowserSkill(BaseSkill):
    def handle(self, text, player):
        if "open browser" in text.lower():
            try:
                webbrowser.open_new_tab("https://www.google.com")
                return True, "Opening the browser"
            except Exception:
                return True, "Failed to open the browser"
        return False, None
# skills/tell_time.py

class TellTimeSkill(BaseSkill):
    def handle(self, text, player):
        if "time" in text.lower():
            now = datetime.now().strftime("%I:%M %p")
            return True, f"The current time is {now}"
        return False, None
# skills/open_youtube.py


class OpenYouTubeSkill(BaseSkill):
    def handle(self, text, player):
        if "youtube" in text.lower():
            try:
                webbrowser.open_new_tab("https://www.youtube.com")
                return True, "Opening YouTube"
            except Exception:
                return True, "Failed to open YouTube"
        return False, None
