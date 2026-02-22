import sys
import asyncio
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QTextEdit, QLineEdit, QPushButton
)
from PySide6.QtCore import Qt


class DesktopApp(QWidget):
    def __init__(self, bus, engine):
        super().__init__()

        self.bus = bus
        self.engine = engine

        self.setWindowTitle("MOON Assistant")
        self.resize(500, 600)

        layout = QVBoxLayout(self)

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)

        self.input = QLineEdit()
        self.input.returnPressed.connect(self.send_text)

        self.btn = QPushButton("Send")
        self.btn.clicked.connect(self.send_text)

        layout.addWidget(self.chat)
        layout.addWidget(self.input)
        layout.addWidget(self.btn)

        # subscribe to assistant output
        self.bus.subscribe("assistant_text", self.display_ai)

    # ------------------------------
    # USER → ENGINE
    # ------------------------------
    def send_text(self):
        text = self.input.text().strip()
        if not text:
            return

        self.chat.append(f"You: {text}")
        self.input.clear()

        asyncio.create_task(self.engine.process(text))

    # ------------------------------
    # ENGINE → UI
    # ------------------------------
    def display_ai(self, text):
        self.chat.append(f"AI: {text}")