# ui/main_window.py
from PySide6.QtWidgets import QTextEdit, QLineEdit, QHBoxLayout
import asyncio
import threading

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
)
from PySide6.QtCore import Qt, Slot   # ← Add Slot here
from PySide6.QtGui import QFont

from ui.face_widget import FaceWidget


class MainWindow(QMainWindow):
    def __init__(self, assistant):
        super().__init__()

        self.assistant = assistant

        self.setWindowTitle("MOON Assistant")
        self.setMinimumSize(420, 600)

        # ===== Central Widget =====
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setAlignment(Qt.AlignCenter)

        # ===== Face =====
        self.face = FaceWidget("assets/face.png")
        layout.addWidget(self.face, alignment=Qt.AlignCenter)

        # ===== Chat History =====
        self.chat_box = QTextEdit()
        self.chat_box.setReadOnly(True)
        self.chat_box.setMinimumHeight(180)
        layout.addWidget(self.chat_box)

        # ===== Input Row =====
        input_row = QHBoxLayout()

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type a message...")
        self.input_field.returnPressed.connect(self.send_text)

        self.btn_send = QPushButton("Send")
        self.btn_send.clicked.connect(self.send_text)

        input_row.addWidget(self.input_field)
        input_row.addWidget(self.btn_send)

        layout.addLayout(input_row)

        # ===== Status Label =====
        self.status = QLabel("Ready")
        self.status.setFont(QFont("Segoe UI", 12))
        self.status.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status)

        # ===== Start Button =====
        self.btn_start = QPushButton("🎙 Start Listening")
        self.btn_start.clicked.connect(self.start_assistant)
        layout.addWidget(self.btn_start)

    # =============================

    def start_assistant(self):
        self.status.setText("Listening...")
        self.assistant.start()

    # ===========================
    def send_text(self):
        text = self.input_field.text().strip()
        if not text:
            return

        self.append_chat("You", text)
        self.input_field.clear()

        # run assistant async safely
        threading.Thread(
            target=lambda: asyncio.run(self.assistant.process_input(text)),
            daemon=True,
        ).start()

    # ===========================
    @Slot(str, str)                     # ← This is the critical line
    def append_chat(self, sender, message):
        if not message:
            return
        self.chat_box.append(f"<b>{sender}:</b> {message}")
        # Optional: auto-scroll to bottom
        self.chat_box.verticalScrollBar().setValue(
            self.chat_box.verticalScrollBar().maximum()
        )