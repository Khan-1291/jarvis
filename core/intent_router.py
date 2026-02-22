from difflib import SequenceMatcher


INTENTS = {
    "aircraft_query": [
        "aircraft",
        "planes nearby",
        "air traffic",
        "what is flying",
        "flight radar",
        "sky activity"
    ],
    "system_control": [
        "shutdown",
        "restart",
        "sleep",
        "turn off"
    ]
}


def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def detect_intent(text):
    best_intent = None
    best_score = 0

    for intent, phrases in INTENTS.items():
        for phrase in phrases:
            score = similarity(text, phrase)
            if score > best_score:
                best_score = score
                best_intent = intent

    if best_score > 0.5:
        return best_intent

    return None
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
