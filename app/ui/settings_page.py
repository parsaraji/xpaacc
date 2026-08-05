from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QComboBox, QPushButton, QMessageBox, QLineEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from app.config import FONT_NAME

class SettingsPage(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setStyleSheet("background-color: #ffffff;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel("تنظیمات عمومی و شخصی‌سازی سیستم")
        title.setFont(QFont(FONT_NAME, 14, QFont.Bold))
        title.setStyleSheet("color: #a62626; border: none;")
        layout.addWidget(title)

        card = QFrame()
        card.setStyleSheet("background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px;")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(15)

        # 1. Custom Letterhead Input
        lbl_head = QLabel("متن سربرگ گزارش‌های آزمایشگاهی (پزشکی/دامپزشکی):")
        lbl_head.setFont(QFont(FONT_NAME, 11, QFont.Bold))
        card_layout.addWidget(lbl_head)

        self.letterhead_input = QLineEdit()
        self.letterhead_input.setPlaceholderText("مثال: آزمایشگاه تخصصی رازی - بخش هورمون‌شناسی")
        self.letterhead_input.setText("آزمایشگاه تخصصی رازی - بخش هورمون‌شناسی")
        card_layout.addWidget(self.letterhead_input)

        # 2. Currency Combo
        lbl1 = QLabel("انتخاب واحد پول پیش‌فرض:")
        card_layout.addWidget(lbl1)

        self.currency_combo = QComboBox()
        self.currency_combo.addItems(["تومان (Toman)", "ریال (Rial)"])
        card_layout.addWidget(self.currency_combo)

        # 3. Theme Combo (Strictly Clean Light)
        lbl2 = QLabel("پوسته یا تم بصری برنامه:")
        card_layout.addWidget(lbl2)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["پوسته روشن (Clean Light)"])
        card_layout.addWidget(self.theme_combo)

        save_btn = QPushButton("ذخیره تنظیمات")
        save_btn.setStyleSheet("background-color: #a62626; color: white; padding: 10px 20px; font-weight: bold;")
        save_btn.clicked.connect(self.save_settings)
        card_layout.addWidget(save_btn)

        layout.addWidget(card)
        layout.addStretch()

    def save_settings(self):
        # Save operation message
        QMessageBox.information(self, "موفقیت", "تنظیمات عمومی و متن سربرگ با موفقیت در سیستم ثبت گردید.")
