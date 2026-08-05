from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont
from app.config import FONT_NAME
from app.database.session import get_db_session
from app.models.customer import Customer
from app.models.laboratory_report import LaboratoryReport
from app.models.transaction import FinancialTransaction
from decimal import Decimal

class DashboardPage(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        header_layout = QHBoxLayout()
        title_lbl = QLabel("میز کار و داشبورد مدیریتی")
        title_lbl.setFont(QFont(FONT_NAME, 16, QFont.Bold))
        title_lbl.setStyleSheet("color: #1f2937;")
        header_layout.addWidget(title_lbl)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        self.cards_grid = QGridLayout()
        self.cards_grid.setSpacing(15)

        self.load_dashboard_summaries()
        layout.addLayout(self.cards_grid)

        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)

        recent_panel = QFrame()
        recent_panel.setStyleSheet("background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px;")
        recent_layout = QVBoxLayout(recent_panel)
        recent_layout.setContentsMargins(15, 15, 15, 15)

        recent_title = QLabel("تراکنش‌های مالی اخیر")
        recent_title.setFont(QFont(FONT_NAME, 12, QFont.Bold))
        recent_title.setStyleSheet("color: #1f2937; margin-bottom: 10px;")
        recent_layout.addWidget(recent_title)

        self.recent_table = QTableWidget()
        self.recent_table.setColumnCount(4)
        self.recent_table.setHorizontalHeaderLabels(["مشتری", "نوع", "بدهکار", "بستانکار"])
        self.recent_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.recent_table.setStyleSheet("background-color: #ffffff; border: none; gridline-color: #e5e7eb;")
        self.recent_table.setRowCount(5)
        self.populate_recent_transactions()

        recent_layout.addWidget(self.recent_table)
        bottom_layout.addWidget(recent_panel, stretch=3)

        quick_panel = QFrame()
        quick_panel.setFixedWidth(280)
        quick_panel.setStyleSheet("background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px;")
        quick_layout = QVBoxLayout(quick_panel)
        quick_layout.setContentsMargins(15, 15, 15, 15)
        quick_layout.setSpacing(12)

        quick_title = QLabel("دسترسی سریع")
        quick_title.setFont(QFont(FONT_NAME, 12, QFont.Bold))
        quick_title.setStyleSheet("color: #0284c7;")
        quick_layout.addWidget(quick_title)

        actions = [
            ("افزودن مشتری جدید", 2),
            ("وارد کردن فایل XPS", 4),
            ("حساب مشتریان", 5),
            ("پشتیبان‌گیری", 9),
            ("تنظیمات برنامه", 10)
        ]

        for label, idx in actions:
            btn = QPushButton(label)
            btn.setFont(QFont(FONT_NAME, 11))
            btn.setMinimumHeight(42)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f9fafb;
                    border: 1px solid #e5e7eb;
                    border-radius: 6px;
                    color: #4b5563;
                    text-align: right;
                    padding-right: 15px;
                }
                QPushButton:hover {
                    background-color: #f3f4f6;
                    border-color: #0284c7;
                    color: #0284c7;
                }
            """)
            btn.clicked.connect(lambda checked=False, index=idx: self.main_window.navigate_to_page(index))
            quick_layout.addWidget(btn)

        quick_layout.addStretch()
        bottom_layout.addWidget(quick_panel, stretch=1)

        layout.addLayout(bottom_layout)

    def load_dashboard_summaries(self):
        tot_custs = 0
        tot_reports = 0
        tot_debit = Decimal("0.00")
        tot_credit = Decimal("0.00")

        with get_db_session() as s:
            tot_custs = s.query(Customer).count()
            tot_reports = s.query(LaboratoryReport).count()

            for cust in s.query(Customer).all():
                bal = cust.current_balance or Decimal("0.00")
                if bal > 0:
                    tot_debit += bal
                elif bal < 0:
                    tot_credit += abs(bal)

        self.create_metric_card(0, 0, "تعداد کل مشتریان", str(tot_custs), "#0284c7")
        self.create_metric_card(0, 1, "تعداد گزارش‌های ثبت‌شده", str(tot_reports), "#0284c7")
        self.create_metric_card(0, 2, "گزارش‌های جدید امروز", "۲", "#0284c7")
        self.create_metric_card(1, 0, "مانده کل بدهکاران", f"{tot_debit:,.0f} تومان", "#ef4444")
        self.create_metric_card(1, 1, "مانده کل بستانکاران", f"{tot_credit:,.0f} تومان", "#10b981")
        self.create_metric_card(1, 2, "اسناد نیازمند بررسی", "۰", "#f59e0b")

    def create_metric_card(self, row, col, title, value, accent_color):
        card = QFrame()
        card.setMinimumHeight(100)
        card.setStyleSheet(f"""
            background-color: #ffffff;
            border: 1px solid #e5e7eb;
            border-left: 5px solid {accent_color};
            border-radius: 6px;
        """)

        c_layout = QVBoxLayout(card)
        c_layout.setContentsMargins(12, 12, 12, 12)

        t_lbl = QLabel(title)
        t_lbl.setFont(QFont(FONT_NAME, 11))
        t_lbl.setStyleSheet("color: #4b5563; border: none;")

        v_lbl = QLabel(value)
        v_lbl.setFont(QFont(FONT_NAME, 15, QFont.Bold))
        v_lbl.setStyleSheet("color: #111827; border: none;")

        c_layout.addWidget(t_lbl)
        c_layout.addWidget(v_lbl)

        self.cards_grid.addWidget(card, row, col)

    def populate_recent_transactions(self):
        with get_db_session() as s:
            recent_txs = s.query(FinancialTransaction).order_by(FinancialTransaction.id.desc()).limit(5).all()
            for idx, tx in enumerate(recent_txs):
                cust = tx.customer
                cust_name = cust.display_name if cust else "ناشناس"

                self.recent_table.setItem(idx, 0, QTableWidgetItem(cust_name))
                self.recent_table.setItem(idx, 1, QTableWidgetItem(tx.transaction_type))
                self.recent_table.setItem(idx, 2, QTableWidgetItem(f"{tx.debit_amount or 0:,.0f}"))
                self.recent_table.setItem(idx, 3, QTableWidgetItem(f"{tx.credit_amount or 0:,.0f}"))
