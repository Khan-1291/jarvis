# skills/reminder_skill.py
import threading
from datetime import datetime, timedelta
from plyer import notification
from skills.base_skill import BaseSkill

class ReminderSkill(BaseSkill):
    reminders = []

    def handle(self, text, player):
        text_lower = text.lower()
        try:
            if "remind me to" in text_lower:
                parts = text_lower.split("remind me to")[1].strip().split(" at ")
                task = parts[0]
                time_str = parts[1] if len(parts) > 1 else None

                if time_str:
                    remind_time = datetime.strptime(time_str, "%H:%M")
                    delta = (remind_time - datetime.now()).total_seconds()
                    if delta < 0:
                        delta += 86400  # next day
                    threading.Timer(delta, lambda: notification.notify(title="Jarvis Reminder", message=task)).start()
                    return True, f"Reminder set for {time_str}: {task}"
        except Exception as e:
            return True, f"Error: {e}"
        return False, None
