# skills/web_automation_skill.py
import webbrowser
from skills.base_skill import BaseSkill

class WebAutomationSkill(BaseSkill):
    def handle(self, text, player):
        text_lower = text.lower()
        try:
            if "search" in text_lower:
                query = text_lower.split("search")[1].strip()
                url = f"https://www.google.com/search?q={query}"
                webbrowser.open(url)
                return True, f"Searching Google for {query}"
            elif "open website" in text_lower:
                url = text_lower.split("open website")[1].strip()
                if not url.startswith("http"):
                    url = "https://" + url
                webbrowser.open(url)
                return True, f"Opening {url}"
        except Exception as e:
            return True, f"Error: {e}"
        return False, None
