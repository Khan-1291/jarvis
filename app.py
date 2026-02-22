# app.py

#from curses import window
import sys
from PySide6.QtWidgets import QApplication

from core import assistant
from ui.modren_mainwindow import MainWindow
from main import AssistantFactory  # we will create this


def load_styles(app):
    with open("ui/styles.qss", "r") as f:
        app.setStyleSheet(f.read())


def main():
    app = QApplication(sys.argv)

    load_styles(app)

    assistant = AssistantFactory.create()

    window = MainWindow(assistant)
    assistant.window = window  # ⭐ IMPORTANT
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()