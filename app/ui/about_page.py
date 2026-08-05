from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from app.config import FONT_NAME, APP_TITLE

class AboutPage(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setStyleSheet("background-color: #ffffff;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        card = QFrame()
        card.setStyleSheet("background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px;")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setAlignment(Qt.AlignCenter)
        card_layout.setSpacing(15)

        title = QLabel(APP_TITLE)
        title.setFont(QFont(FONT_NAME, 16, QFont.Bold))
        title.setStyleSheet("color: #a62626; border: none;")
        card_layout.addWidget(title)

        version = QLabel("نسخه تولیدی نهایی: v1.0.0 (پایدار)")
        version.setFont(QFont(FONT_NAME, 11))
        version.setStyleSheet("color: #4b5563; border: none;")
        card_layout.addWidget(version)

        desc = QLabel("این سامانه یک بستر کاملا آفلاین، یکپارچه و هوشمند برای ورود اسناد آزمایشگاهی با فرمت‌های XPS، OXPS و PDF، استخراج مکانی داده‌ها، آرشیو هوشمند اطلاعات بیماران و مدیریت حساب‌های مالی مشتریان به صورت راست‌به‌چپ (RTL) می‌باشد.")
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet("line-height: 1.8; color: #2b2b2b; max-width: 600px; border: none;")
        card_layout.addWidget(desc)

        layout.addWidget(card)
        layout.addStretch()
