# assistant.py
import re
import random

from core.command_router import CommandRouter
from core.response_formatter import format_response
from core.security import is_risky
from core.state_manager import StateManager
from logs.logger import log_info, log_warning
from core.context_manager import ContextManager
from core.monitring_engine import MonitoringEngine

from monitors.system_monitors import cpu_monitor


class Assistant:
    def __init__(self, stt, tts, llm, skills, player, memory=None):
        self.stt = stt
        self.tts = tts
        self.llm = llm
        
        self.player = player
        self.router = CommandRouter(skills)
        self.state = StateManager()
        self.context = ContextManager()
        self.monitor = MonitoringEngine()
        self.monitor.add_task(lambda: cpu_monitor(self), interval=10)
        self.monitor.start()

        self.memory = memory

        log_info("Assistant initialized with enhanced personal memory features.")

    async def process_input(self, text: str):
        # Extract and store facts before anything else
        self.extract_and_store_facts(text)
        
        result = self.router.route(text, self.player)
        
        # ────────────────────────────────────────────────
        # SKILL / COMMAND HANDLED
        # ────────────────────────────────────────────────
        if result.get("handled"):
            intent = result.get("intent")
            data = result.get("data")
            self.context.update(intent=intent, data=data)

            if result.get("response"):
                response = format_response(result["response"])

                # Personalize if possible
                response = self.personalize_response(response)

                # UI callback
                if hasattr(self, "ui_callback"):
                    self.ui_callback(response)

                # Store conversation
                if self.memory:
                    self.memory.add_conversation(text, response)

                self.tts(response, self.player)

            return

        # ────────────────────────────────────────────────
        # NAME QUICK CHECK (special case)
        # ────────────────────────────────────────────────
        if self.memory and any(q in text.lower() for q in ["what is my name", "what's my name"]):
            name = self.memory.get("name")
            if name:
                response = f"Your name is {name}."
                self.tts(response, self.player)
                if hasattr(self, "ui_callback"):
                    self.ui_callback(response)
                return

        # ────────────────────────────────────────────────
        # FALLBACK TO LLM
        # ────────────────────────────────────────────────
        context = self.get_personal_context()
        enhanced_prompt = (
            f"{context}\n\n"
            f"User: {text}\n"
            "Respond in a friendly, natural, human-like way. "
            "Use casual language when it fits. Be warm and slightly playful sometimes."
        )

        response = self.llm(enhanced_prompt, memory=self.memory)
        response = format_response(response)

        # Final personalization
        response = self.personalize_response(response)

        # UI
        if hasattr(self, "ui_callback"):
            self.ui_callback(response)

        # Store conversation
        if self.memory:
            self.memory.add_conversation(text, response)

        self.tts(response, self.player)

        log_info(f"LLM Response: {response}")

    def extract_and_store_facts(self, text: str):
        if not self.memory:
            return

        text_lower = text.lower()

        # My name is ...
        if m := re.search(r"my name is (\w+)", text_lower):
            name = m.group(1).capitalize()
            self.memory.remember("name", name)

        # I like ...
        if m := re.search(r"i like (.+)", text_lower):
            interest = m.group(1).strip().capitalize()
            self.memory.remember("likes", interest)  # auto-appends if list

        # My favorite ... is ...
        if m := re.search(r"my favorite (.+?) is (.+)", text_lower):
            category = m.group(1).strip().replace(" ", "_")
            value = m.group(2).strip().capitalize()
            self.memory.remember(f"favorite_{category}", value)

        # Birthday
        if m := re.search(r"my birthday is (on )?(.+)", text_lower):
            birthday = m.group(2).strip().capitalize()
            self.memory.remember("birthday", birthday)

        # I live in ...
        if m := re.search(r"i live in (.+)", text_lower):
            location = m.group(1).strip().title()
            self.memory.remember("location", location)

        # My hobby / hobbies are ...
        if m := re.search(r"my hobb(?:y|ies) (?:is|are) (.+)", text_lower):
            hobby = m.group(1).strip().capitalize()
            self.memory.remember("hobbies", hobby)  # auto-appends

    def get_personal_context(self) -> str:
        if not self.memory:
            return ""

        try:
            facts = self.memory.get_all_facts()
        except Exception as e:
            log_warning(f"Failed to read memory facts: {e}")
            return ""

        lines = []

        # Core identity
        if name := facts.get("name"):
            lines.append(f"The user's name is {name}.")

        if loc := facts.get("location"):
            lines.append(f"The user lives in {loc}.")

        if bday := facts.get("birthday"):
            lines.append(f"Birthday: {bday}.")

        # Lists
        for key in ["likes", "hobbies"]:
            if val := facts.get(key):
                if isinstance(val, list) and val:
                    lines.append(f"The user {key}: {', '.join(val)}.")

        # Favorites
        for key, value in facts.items():
            if key.startswith("favorite_") and value:
                category = key.replace("favorite_", "").replace("_", " ").title()
                lines.append(f"Favorite {category}: {value}.")

        if not lines:
            return "No personal context remembered yet."

        return "\n".join(lines)

    def personalize_response(self, response: str) -> str:
        if not self.memory:
            return response

        # Replace "sir" with name if known
        if name := self.memory.get("name"):
            if "sir" in response.lower():
                response = re.sub(r"\bsir\b", name, response, flags=re.IGNORECASE)

        # Occasional human touches
        if random.random() > 0.7:
            touches = [
                " By the way, hope you're having a great day!",
                " Haha, that's cool!",
                " Just saying…",
                " You know what I mean? 😄",
            ]
            response += random.choice(touches)

        return response