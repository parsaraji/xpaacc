from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QFrame, QFileDialog
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
        self.setStyleSheet("background-color: #ffffff;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel("پشتیبان‌گیری و درون‌ریزی اطلاعات سیستم")
        title.setFont(QFont(FONT_NAME, 14, QFont.Bold))
        title.setStyleSheet("color: #a62626; border: none;")
        layout.addWidget(title)

        # Actions Card
        card = QFrame()
        card.setStyleSheet("background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px;")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(15)

        desc = QLabel("جهت پشتیبان‌گیری کامل از پایگاه داده و فایل‌های استخراج شده روی دکمه زیر کلیک نمایید. همچنین می‌توانید یک فایل پشتیبان قبلی را جهت بازیابی کامل اطلاعات درون‌ریزی کنید.")
        desc.setWordWrap(True)
        desc.setFont(QFont(FONT_NAME, 11))
        desc.setStyleSheet("color: #4b5563; line-height: 1.6; border: none;")
        card_layout.addWidget(desc)

        # Buttons layout
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        backup_btn = QPushButton("برون‌بری نسخه پشتیبان (فشرده ZIP)")
        backup_btn.setFont(QFont(FONT_NAME, 11, QFont.Bold))
        backup_btn.setStyleSheet("background-color: #a62626; color: white; padding: 12px 24px; border-radius: 6px;")
        backup_btn.clicked.connect(self.run_backup)
        btn_layout.addWidget(backup_btn)

        restore_btn = QPushButton("درون‌ریزی و بازیابی فایل پشتیبان...")
        restore_btn.setFont(QFont(FONT_NAME, 11, QFont.Bold))
        restore_btn.setStyleSheet("background-color: #0284c7; color: white; padding: 12px 24px; border-radius: 6px;")
        restore_btn.clicked.connect(self.run_restore)
        btn_layout.addWidget(restore_btn)

        card_layout.addLayout(btn_layout)

        layout.addWidget(card)
        layout.addStretch()

    def run_backup(self):
        with get_db_session() as s:
            service = BackupService(s)
            try:
                dest = service.create_backup()
                QMessageBox.information(
                    self, "موفقیت",
                    f"نسخه پشتیبان به همراه بانک اطلاعاتی و اسناد با موفقیت تهیه و ذخیره گردید:\n{dest}"
                )
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در پشتیبان‌گیری: {str(e)}")

    def run_restore(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self, "انتخاب فایل پشتیبان جهت درون‌ریزی", "", "ZIP Backups (*.zip)"
        )
        if not filepath:
            return

        reply = QMessageBox.question(
            self, "تأیید درون‌ریزی",
            "آیا مطمئن هستید؟ درون‌ریزی فایل پشتیبان باعث جایگزینی کامل اطلاعات جاری سیستم با داده‌های فایل پشتیبان خواهد شد.",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            with get_db_session() as s:
                service = BackupService(s)
                try:
                    service.restore_backup(filepath)
                    QMessageBox.information(self, "موفقیت", "درون‌ریزی و بازیابی دیتابیس با موفقیت به پایان رسید.")
                except Exception as e:
                    QMessageBox.critical(self, "خطا در درون‌ریزی", str(e))
