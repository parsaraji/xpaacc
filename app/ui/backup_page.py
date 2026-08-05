from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from app.config import FONT_NAME
from app.database.session import get_db_session
from app.services.backup_service import BackupService
import os

class BackupPage(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel("پشتیبان‌گیری و بازیابی اطلاعات سیستم")
        title.setFont(QFont(FONT_NAME, 14, QFont.Bold))
        layout.addWidget(title)

        # Actions Card
        card = QFrame()
        card.setStyleSheet("background-color: #1a202c; border: 1px solid #2d3748; border-radius: 8px;")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(15)

        desc = QLabel("جهت جلوگیری از حذف ناخواسته داده‌ها و بروز حوادث فیزیکی، توصیه می‌گردد به صورت منظم از اطلاعات و فایل‌های آرشیو سیستم نسخه پشتیبان تهیه فرمایید.")
        desc.setWordWrap(True)
        desc.setFont(QFont(FONT_NAME, 11))
        desc.setStyleSheet("color: #a0aec0; line-height: 1.6;")
        card_layout.addWidget(desc)

        backup_btn = QPushButton("تهیه نسخه پشتیبان (فشرده ZIP)")
        backup_btn.setFont(QFont(FONT_NAME, 11, QFont.Bold))
        backup_btn.setStyleSheet("background-color: #319795; color: white; padding: 12px 24px; border-radius: 6px;")
        backup_btn.clicked.connect(self.run_backup)
        card_layout.addWidget(backup_btn)

        layout.addWidget(card)
        layout.addStretch()

    def run_backup(self):
        with get_db_session() as s:
            service = BackupService(s)
            try:
                dest = service.create_backup()
                QMessageBox.information(
                    self, "موفقیت",
                    f"نسخه پشتیبان با موفقیت تهیه و در مسیر زیر ذخیره گردید:\n{dest}"
                )
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در پشتیبان‌گیری: {str(e)}")
