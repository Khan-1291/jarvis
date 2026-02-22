class ContextManager:
    def __init__(self):
        self.last_intent = None
        self.last_data = None

    def update(self, intent=None, data=None):
        if intent:
            self.last_intent = intent
        if data is not None:
            self.last_data = data

    def clear(self):
        self.last_intent = None
        self.last_data = None
