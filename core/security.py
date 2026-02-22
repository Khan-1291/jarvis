RISKY_KEYWORDS = [
    "delete",
    "remove",
    "shutdown",
    "format",
    "factory reset",
    "uninstall"
]

def is_risky(text):
    return any(word in text.lower() for word in RISKY_KEYWORDS)
