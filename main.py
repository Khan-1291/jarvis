# main.py
import asyncio
import threading

from core.assistant import Assistant
from skills.aircraft_skill import AircraftSkill
from skills.open_browser import OpenBrowserSkill, TellTimeSkill, OpenYouTubeSkill
from skills.file_manager_skill import FileManagerSkill
from skills.app_launcher_skill import AppLauncherSkill
from skills.system_control_skill import SystemControlSkill
from skills.web_automation_skill import WebAutomationSkill
from skills.reminder_skill import ReminderSkill
from skills.media_skill import MediaSkill
from skills.memory_skill import MemorySkill
from skills.whatsapp_skill import WhatsAppSkill
from skills.spotify import SpotifySkill
from skills.system_skill import SystemSkill

from memory.memory import Memory
from voice.speech_to_text import record_voice
from ui.main_window import VoiceImagePlayer, edge_speak
from llm.groq_client import get_response


memory = Memory()  # Assuming Memory now supports persistence, e.g., via SQLite


# ================= VOICE LOOP =================

async def voice_listener(assistant):
    while True:
        user_text = await asyncio.to_thread(record_voice)
        if user_text:
            await assistant.process_input(user_text)


async def text_listener(assistant):
    while True:
        user_text = await asyncio.to_thread(input, "You: ")
        if user_text.strip():
            await assistant.process_input(user_text)


async def ai_loop(assistant):
    await asyncio.gather(
        voice_listener(assistant),
        text_listener(assistant)
    )


# ================= FACTORY =================

class AssistantFactory:
    @staticmethod
    def create():
        player = VoiceImagePlayer("assets/face.png", size=(900, 900))
    
        skills = [
            AircraftSkill(),
            OpenBrowserSkill(),
            OpenYouTubeSkill(),
            TellTimeSkill(),
            WhatsAppSkill(),
            FileManagerSkill(),
            AppLauncherSkill(),
            SystemControlSkill(),
            WebAutomationSkill(),
            ReminderSkill(),
            MediaSkill(),
            MemorySkill(memory),
            SpotifySkill(),
            SystemSkill(),
        ]

        assistant = Assistant(
            stt=record_voice,
            tts=edge_speak,
            llm=get_response,
            skills=skills,
            player=player,
            memory=memory  # Now always include memory for long-term persistence
        )

        # ⭐ attach runner to assistant
        def start_runner():
            def thread_target():
                asyncio.run(ai_loop(assistant))

            threading.Thread(target=thread_target, daemon=True).start()

        assistant.start = start_runner

        def ui_callback(text):
            # safe UI update later (Qt thread)
            try:
                from PySide6.QtCore import QMetaObject, Qt, Q_ARG
                from PySide6.QtWidgets import QApplication

                app = QApplication.instance()
                if hasattr(assistant, "window"):
                    QMetaObject.invokeMethod(
                        assistant.window,
                        "append_chat",
                        Qt.QueuedConnection,
                        Q_ARG(str, "MOON"),
                        Q_ARG(str, text),
                    )
            except Exception:
                pass

        assistant.ui_callback = ui_callback

        return assistant