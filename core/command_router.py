# core/command_router.py

import logging
from core.intent_router import detect_intent


class CommandRouter:
    def __init__(self, skills):
        self.skills = skills

    def route(self, text, player):
        logging.info(f"User Command: {text}")

        intent = detect_intent(text)

        for skill in self.skills:
            try:
                # First: intent-based routing
                if hasattr(skill, "intent") and skill.intent == intent:
                    handled, response = skill.handle(text, player)
                    if handled:
                        return {"handled": True, "response": response}

                # Second: fallback matching inside skill
                handled, response = skill.handle(text, player)
                if handled:
                    return {"handled": True, "response": response}

            except Exception as e:
                logging.error(f"Skill error: {e}")

        # Nothing handled
        return {"handled": False, "response": None}
