from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QComboBox, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from app.config import FONT_NAME

class SettingsPage(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel("تنظیمات عمومی و شخصی‌سازی سیستم")
        title.setFont(QFont(FONT_NAME, 14, QFont.Bold))
        layout.addWidget(title)

        card = QFrame()
        card.setStyleSheet("background-color: #1a202c; border: 1px solid #2d3748; border-radius: 8px;")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(15)

        lbl1 = QLabel("انتخاب واحد پول پیش‌فرض:")
        card_layout.addWidget(lbl1)

        self.currency_combo = QComboBox()
        self.currency_combo.addItems(["تومان (Toman)", "ریال (Rial)"])
        card_layout.addWidget(self.currency_combo)

        lbl2 = QLabel("پوسته یا تم بصری برنامه:")
        card_layout.addWidget(lbl2)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["پوسته تیره (Premium Dark)", "پوسته روشن (Clean Light)"])
        card_layout.addWidget(self.theme_combo)

        save_btn = QPushButton("ذخیره تنظیمات")
        save_btn.setStyleSheet("background-color: #319795; color: white; padding: 10px 20px; font-weight: bold;")
        save_btn.clicked.connect(self.save_settings)
        card_layout.addWidget(save_btn)

        layout.addWidget(card)
        layout.addStretch()

    def save_settings(self):
        # Dynamically switch stylesheets if Light is selected
        sel_theme = self.theme_combo.currentText()
        if "روشن" in sel_theme:
            self.main_window.setStyleSheet("""
                QMainWindow { background-color: #f7fafc; }
                QWidget { color: #2d3748; font-family: 'Vazirmatn'; }
                QFrame#Sidebar { background-color: #edf2f7; border-right: 1px solid #cbd5e0; }
                QListWidget#NavList::item { color: #4a5568; }
                QListWidget#NavList::item:selected { background-color: #319795; color: white; }
            """)
        else:
            self.main_window.setStyleSheet("""
                QMainWindow { background-color: #1a1e24; }
                QWidget { color: #e3e8f0; font-family: 'Vazirmatn'; }
                QFrame#Sidebar { background-color: #11151a; border-right: 1px solid #232d38; }
                QListWidget#NavList::item { color: #a0aec0; }
                QListWidget#NavList::item:selected { background-color: #319795; color: white; }
            """)
        QMessageBox.information(self, "موفقیت", "تنظیمات عمومی ذخیره و اعمال گردید.")
