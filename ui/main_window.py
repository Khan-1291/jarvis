import tkinter as tk
from PIL import Image, ImageTk
import threading
import subprocess

import asyncio
from core.response_formatter import format_response
import edge_tts
from playsound import playsound
import os
import uuid
import threading



class VoiceImagePlayer:
    def __init__(self, image_path, size=(500, 500)):
        self.root = tk.Tk()
        self.root.title("Moon Assistant")

        # Load image
        self.image = Image.open(image_path)
        self.image = self.image.resize(size)
        self.photo = ImageTk.PhotoImage(self.image)

        self.label = tk.Label(self.root, image=self.photo)
        self.label.pack()

        # Log area
        self.log = tk.Text(self.root, height=10)
        self.log.pack(fill="both", expand=True)

    def write_log(self, text):
        # Thread-safe UI update
        self.root.after(0, self._append_log, text)

    def _append_log(self, text):
        self.log.insert("end", text + "\n")
        self.log.see("end")



def edge_speak(text, player=None):
    async def speak_async():
        filename = f"{uuid.uuid4()}.mp3"

        communicate = edge_tts.Communicate(
            text=format_response(text),
            voice="en-US-AriaNeural"
        )

        await communicate.save(filename)
        playsound(filename)
        os.remove(filename)

    def run():
        asyncio.run(speak_async())

    threading.Thread(target=run, daemon=True).start()
