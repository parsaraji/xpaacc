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
        self.setStyleSheet("background-color: #ffffff;")

        title = QLabel("ورود و پردازش فایل‌های آزمایشگاهی جدید (XPS/OXPS/PDF)")
        title.setFont(QFont(FONT_NAME, 14, QFont.Bold))
        title.setStyleSheet("color: #a62626;")
        layout.addWidget(title)

        # Upload card area
        self.upload_card = QFrame()
        self.upload_card.setMinimumHeight(350)
        self.upload_card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 2px dashed #cccccc;
                border-radius: 12px;
            }
        """)

        drop_layout = QVBoxLayout(self.upload_card)
        drop_layout.setAlignment(Qt.AlignCenter)
        drop_layout.setSpacing(15)

        info_lbl = QLabel("جهت بارگذاری و استخراج هوشمند اطلاعات آزمایش، فایل خود را انتخاب نمایید")
        info_lbl.setFont(QFont(FONT_NAME, 12))
        info_lbl.setAlignment(Qt.AlignCenter)
        info_lbl.setStyleSheet("color: #4b5563; border: none;")
        drop_layout.addWidget(info_lbl)

        select_btn = QPushButton("انتخاب فایل گزارش...")
        select_btn.setFont(QFont(FONT_NAME, 11, QFont.Bold))
        select_btn.setStyleSheet("""
            QPushButton {
                background-color: #a62626;
                color: white;
                padding: 10px 24px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8a1d1d;
            }
        """)
        select_btn.clicked.connect(self.choose_file)
        drop_layout.addWidget(select_btn)

        layout.addWidget(self.upload_card)
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
