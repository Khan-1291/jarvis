import psutil
import socket
import datetime
import platform
from skills.base_skill import BaseSkill


class SystemSkill(BaseSkill):
    intent = "system"

    # --------------------------------------------------
    # MAIN HANDLER
    # --------------------------------------------------
    def handle(self, text, player):
        text = text.lower()

        # battery
        if "battery" in text:
            return True, self._battery_status()

        # cpu
        if "cpu" in text:
            return True, self._cpu_status()

        # ram
        if "ram" in text or "memory" in text:
            return True, self._ram_status()

        # disk
        if "disk" in text or "storage" in text:
            return True, self._disk_status()

        # internet
        if "internet" in text or "connection" in text:
            return True, self._internet_status()

        # time
        if "time" in text:
            return True, self._time_status()

        # date
        if "date" in text:
            return True, self._date_status()

        # system info
        if "system info" in text:
            return True, self._system_info()

        return False, None

    # --------------------------------------------------
    # BATTERY
    # --------------------------------------------------
    def _battery_status(self):
        battery = psutil.sensors_battery()

        if battery is None:
            return "Battery not detected."

        percent = battery.percent
        plugged = battery.power_plugged

        if plugged:
            return f"Battery at {percent}% and charging."
        else:
            return f"Battery at {percent}% and discharging."

    # --------------------------------------------------
    # CPU
    # --------------------------------------------------
    def _cpu_status(self):
        usage = psutil.cpu_percent(interval=1)
        return f"CPU usage is {usage}%."

    # --------------------------------------------------
    # RAM
    # --------------------------------------------------
    def _ram_status(self):
        mem = psutil.virtual_memory()
        return f"RAM usage is {mem.percent}%."

    # --------------------------------------------------
    # DISK
    # --------------------------------------------------
    def _disk_status(self):
        disk = psutil.disk_usage('/')
        return f"Disk usage is {disk.percent}%."

    # --------------------------------------------------
    # INTERNET
    # --------------------------------------------------
    def _internet_status(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return "Internet connection is active."
        except:
            return "No internet connection."

    # --------------------------------------------------
    # TIME
    # --------------------------------------------------
    def _time_status(self):
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The time is {now}."

    # --------------------------------------------------
    # DATE
    # --------------------------------------------------
    def _date_status(self):
        today = datetime.date.today().strftime("%B %d, %Y")
        return f"Today is {today}."

    # --------------------------------------------------
    # SYSTEM INFO
    # --------------------------------------------------
    def _system_info(self):
        os_name = platform.system()
        os_version = platform.release()
        machine = platform.machine()

        return f"You are running {os_name} {os_version} on {machine} architecture."
