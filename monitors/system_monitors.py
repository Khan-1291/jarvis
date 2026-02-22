import psutil
from core.response_formatter import format_response


def cpu_monitor(assistant):
    cpu = psutil.cpu_percent(interval=1)

    if cpu > 85:
        message = format_response("Warning. CPU usage is critically high")
        assistant.tts(message, assistant.player)
