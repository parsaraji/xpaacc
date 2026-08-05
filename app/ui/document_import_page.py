from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from app.config import FONT_NAME
import os

class DocumentImportPage(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel("ورود و پردازش فایل‌های آزمایشگاهی جدید (XPS/OXPS/PDF)")
        title.setFont(QFont(FONT_NAME, 14, QFont.Bold))
        layout.addWidget(title)

        self.drop_zone = QFrame()
        self.drop_zone.setMinimumHeight(350)
        self.drop_zone.setStyleSheet("""
            QFrame {
                background-color: #1a202c;
                border: 2px dashed #4a5568;
                border-radius: 12px;
            }
            QFrame:hover {
                border-color: #319795;
                background-color: #1e2630;
            }
        """)

        drop_layout = QVBoxLayout(self.drop_zone)
        drop_layout.setAlignment(Qt.AlignCenter)
        drop_layout.setSpacing(15)

        info_lbl = QLabel("فایل گزارش آزمایشگاه را به این بخش بکشید و رها کنید\nیا روی دکمه زیر جهت انتخاب فایل کلیک کنید")
        info_lbl.setFont(QFont(FONT_NAME, 12))
        info_lbl.setAlignment(Qt.AlignCenter)
        info_lbl.setStyleSheet("color: #a0aec0; line-height: 1.6;")
        drop_layout.addWidget(info_lbl)

        select_btn = QPushButton("انتخاب فایل گزارش...")
        select_btn.setFont(QFont(FONT_NAME, 11, QFont.Bold))
        select_btn.setStyleSheet("""
            background-color: #319795;
            color: white;
            padding: 10px 24px;
            border-radius: 6px;
        """)
        select_btn.clicked.connect(self.choose_file)
        drop_layout.addWidget(select_btn)

        layout.addWidget(self.drop_zone)
        layout.addStretch()

    def choose_file(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self, "انتخاب فایل آزمایشگاهی", "", "Laboratory Documents (*.xps *.oxps *.pdf)"
        )
        if filepath:
            self.load_document_in_viewer(filepath)

    def load_document_in_viewer(self, filepath: str):
        self.main_window.document_viewer_page.load_file(filepath)
        self.main_window.navigate_to_page(14)
