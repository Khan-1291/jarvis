import asyncio
from collections import defaultdict

class EventBus:
    def __init__(self):
        self.subscribers = defaultdict(list)

    def subscribe(self, event_name, callback):
        self.subscribers[event_name].append(callback)

    async def emit(self, event_name, data=None):
        if event_name in self.subscribers:
            for callback in self.subscribers[event_name]:
                if asyncio.iscoroutinefunction(callback):
                    await callback(data)
                else:
                    callback(data)