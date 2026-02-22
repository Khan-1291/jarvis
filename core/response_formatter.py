def format_response(text: str) -> str:
    text = text.strip()

    if not text.lower().endswith("sir.") and not text.lower().endswith("sir"):
        if text.endswith("."):
            text = text[:-1]
        text += ", sir."

    return text
