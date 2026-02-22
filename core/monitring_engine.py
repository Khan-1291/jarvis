import threading
import time


class MonitoringEngine:
    def __init__(self):
        self.tasks = []
        self.running = False

    def add_task(self, func, interval):
        self.tasks.append((func, interval))

    def start(self):
        self.running = True
        for func, interval in self.tasks:
            threading.Thread(
                target=self._run_task,
                args=(func, interval),
                daemon=True
            ).start()

    def _run_task(self, func, interval):
        while self.running:
            try:
                func()
            except Exception as e:
                print("Monitor error:", e)
            time.sleep(interval)

    def stop(self):
        self.running = False
