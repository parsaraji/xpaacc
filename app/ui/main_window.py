import sys
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QStackedWidget,
    QLabel, QPushButton, QFrame, QStyle
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon, QAction
from app.config import APP_TITLE, FONT_NAME

from app.ui.dashboard_page import DashboardPage
from app.ui.customers_page import CustomersPage
from app.ui.customer_form import CustomerForm
from app.ui.customer_profile import CustomerProfile
from app.ui.customer_statement import CustomerStatement
from app.ui.document_import_page import DocumentImportPage
from app.ui.document_viewer import DocumentViewer
from app.ui.extraction_review import ExtractionReview
from app.ui.reports_page import ReportsPage
from app.ui.transactions_page import TransactionsPage
from app.ui.backup_page import BackupPage
from app.ui.settings_page import SettingsPage
from app.ui.about_page import AboutPage
from app.ui.advanced_search_page import AdvancedSearchPage
from app.ui.catalog_page import CatalogPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.setMinimumSize(1200, 800)

        # Apply Central Application Font & RTL Styling
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        # Global Microsoft Premium Clean Light Stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f3f4f6; /* Premium Ivory/Light Gray background */
            }
            QWidget {
                color: #1f2937; /* Clean Charcoal/Dark Gray Text */
                font-family: 'Vazirmatn', 'Segoe UI', Tahoma;
                font-size: 13px;
            }
            QFrame#Sidebar {
                background-color: #ffffff; /* Microsoft Clean Light sidebar */
                border-left: 1px solid #e5e7eb;
            }
            QListWidget#NavList {
                background-color: transparent;
                border: none;
            }
            QListWidget#NavList::item {
                height: 48px;
                padding-left: 15px;
                border-radius: 6px;
                margin-bottom: 4px;
                background-color: transparent;
                color: #4b5563;
            }
            QListWidget#NavList::item:hover {
                background-color: #f3f4f6;
                color: #0284c7; /* Microsoft Blue/Teal */
            }
            QListWidget#NavList::item:selected {
                background-color: #0284c7; /* Blue active item */
                color: #ffffff;
                font-weight: bold;
            }
            QPushButton {
                background-color: #0284c7;
                color: #ffffff;
                border: 1px solid #0284c7;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0369a1;
            }
            QTableWidget {
                background-color: #ffffff;
                gridline-color: #e5e7eb;
                border: 1px solid #e5e7eb;
                color: #1f2937;
            }
            QHeaderView::section {
                background-color: #f9fafb;
                color: #374151;
                padding: 8px;
                font-weight: bold;
                border: 1px solid #e5e7eb;
            }
            QLineEdit, QComboBox, QTextEdit {
                background-color: #ffffff;
                border: 1px solid #d1d5db;
                border-radius: 4px;
                padding: 6px;
                color: #1f2937;
            }
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
                border: 1px solid #0284c7;
            }
        """)

        # Main Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QHBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Sidebar Right-aligned Navigation Frame
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(240)

        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(10)

        # Brand/Logo Header
        brand_label = QLabel(APP_TITLE)
        brand_label.setFont(QFont(FONT_NAME, 13, QFont.Bold))
        brand_label.setWordWrap(True)
        brand_label.setAlignment(Qt.AlignCenter)
        brand_label.setStyleSheet("color: #0284c7; margin-bottom: 20px; line-height: 1.4;")
        sidebar_layout.addWidget(brand_label)

        # Navigation Menu List
        self.nav_list = QListWidget()
        self.nav_list.setObjectName("NavList")

        self.menu_items = [
            "داشبورد",                  # 0
            "مشتریان",                  # 1
            "افزودن مشتری",              # 2
            "گزارش‌های آزمایشگاهی",       # 3
            "ورود فایل XPS",            # 4
            "حساب مشتریان",              # 5
            "دریافت‌ها و پرداخت‌ها",       # 6
            "مدیریت قیمت آزمایشگاهی",     # 7
            "جستجوی پیشرفته",            # 8
            "پشتیبان‌گیری",              # 9
            "تنظیمات",                  # 10
            "درباره برنامه"              # 11
        ]

        for item in self.menu_items:
            self.nav_list.addItem(item)

        self.nav_list.setCurrentRow(0)
        self.nav_list.currentRowChanged.connect(self.on_nav_change)
        sidebar_layout.addWidget(self.nav_list)

        sidebar_layout.addStretch()

        # Footer branding
        footer_brand = QLabel("طراحی شده برای ویندوز")
        footer_brand.setFont(QFont(FONT_NAME, 10))
        footer_brand.setStyleSheet("color: #9ca3af;")
        footer_brand.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(footer_brand)

        main_layout.addWidget(self.sidebar)

        # 2. Left Central Container (Stacked Pages)
        self.pages_container = QStackedWidget()
        main_layout.addWidget(self.pages_container)

        # Instantiate Menu Pages
        self.dashboard_page = DashboardPage(self)             # 0
        self.customers_page = CustomersPage(self)             # 1
        self.customer_form_page = CustomerForm(self)           # 2
        self.reports_page = ReportsPage(self)                 # 3
        self.document_import_page = DocumentImportPage(self)   # 4
        self.transactions_page = TransactionsPage(self)       # 5 & 6
        self.catalog_page = CatalogPage(self)                 # 7
        self.search_page = AdvancedSearchPage(self)           # 8
        self.backup_page = BackupPage(self)                   # 9
        self.settings_page = SettingsPage(self)               # 10
        self.about_page = AboutPage(self)                     # 11

        self.customer_profile_page = CustomerProfile(self)     # 12
        self.customer_statement_page = CustomerStatement(self) # 13
        self.document_viewer_page = DocumentViewer(self)       # 14
        self.extraction_review_page = ExtractionReview(self)   # 15

        # Add them as unique widgets to stacked widget container
        self.pages_container.addWidget(self.dashboard_page)       # 0
        self.pages_container.addWidget(self.customers_page)       # 1
        self.pages_container.addWidget(self.customer_form_page)     # 2
        self.pages_container.addWidget(self.reports_page)           # 3
        self.pages_container.addWidget(self.document_import_page)   # 4
        self.pages_container.addWidget(self.transactions_page)     # 5
        self.pages_container.addWidget(self.catalog_page)          # 6
        self.pages_container.addWidget(self.search_page)            # 7
        self.pages_container.addWidget(self.backup_page)            # 8
        self.pages_container.addWidget(self.settings_page)          # 9
        self.pages_container.addWidget(self.about_page)             # 10
        self.pages_container.addWidget(self.customer_profile_page)  # 11
        self.pages_container.addWidget(self.customer_statement_page)# 12
        self.pages_container.addWidget(self.document_viewer_page)  # 13
        self.pages_container.addWidget(self.extraction_review_page)# 14

        # Clean routing map
        self.page_mapping = {
            0: self.dashboard_page,
            1: self.customers_page,
            2: self.customer_form_page,
            3: self.reports_page,
            4: self.document_import_page,
            5: self.transactions_page,
            6: self.transactions_page,
            7: self.catalog_page,
            8: self.search_page,
            9: self.backup_page,
            10: self.settings_page,
            11: self.about_page,
            12: self.customer_profile_page,
            13: self.customer_statement_page,
            14: self.document_viewer_page,
            15: self.extraction_review_page
        }

    def on_nav_change(self, index: int):
        target_widget = self.page_mapping.get(index, self.dashboard_page)
        self.pages_container.setCurrentWidget(target_widget)

        # Trigger page data updates
        if index == 1:
            self.customers_page.load_customers()
        elif index == 0:
            self.dashboard_page.load_dashboard_summaries()
            self.dashboard_page.populate_recent_transactions()
        elif index == 3:
            self.reports_page.load_reports()
        elif index == 7:
            self.catalog_page.load_catalog()
        elif index in [5, 6]:
            self.transactions_page.load_customers_combo()
            self.transactions_page.load_transactions()

    def navigate_to_page(self, index: int):
        if index < len(self.menu_items):
            self.nav_list.setCurrentRow(index)

        target_widget = self.page_mapping.get(index, self.dashboard_page)
        self.pages_container.setCurrentWidget(target_widget)

        if index == 1:
            self.customers_page.load_customers()
        elif index == 3:
            self.reports_page.load_reports()
        elif index == 7:
            self.catalog_page.load_catalog()
        elif index == 12:
            self.customer_profile_page.load_profile_data()
        elif index == 13:
            self.customer_statement_page.load_statement()
        elif index in [5, 6]:
            self.transactions_page.load_customers_combo()
            self.transactions_page.load_transactions()
