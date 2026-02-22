# ui/face_widget.py

from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class FaceWidget(QLabel):
    def __init__(self, image_path: str):
        super().__init__()

        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(
            260,
            260,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )

        self.setPixmap(pixmap)
        self.setAlignment(Qt.AlignCenter)