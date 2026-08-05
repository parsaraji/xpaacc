from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QTabWidget,
    QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from app.config import FONT_NAME
from app.database.session import get_db_session
from app.models.customer import Customer
from app.models.transaction import FinancialTransaction
from app.models.laboratory_report import LaboratoryReport

class CustomerProfile(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.customer_id = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.header_card = QFrame()
        self.header_card.setStyleSheet("background-color: #1a202c; border: 1px solid #2d3748; border-radius: 8px;")
        h_layout = QHBoxLayout(self.header_card)
        h_layout.setContentsMargins(15, 15, 15, 15)

        self.name_lbl = QLabel("نام مشتری")
        self.name_lbl.setFont(QFont(FONT_NAME, 14, QFont.Bold))
        self.name_lbl.setStyleSheet("color: #ffffff;")
        h_layout.addWidget(self.name_lbl)

        self.code_lbl = QLabel("کد مشتری")
        self.code_lbl.setFont(QFont(FONT_NAME, 11))
        self.code_lbl.setStyleSheet("color: #a0aec0;")
        h_layout.addWidget(self.code_lbl)

        h_layout.addStretch()

        self.bal_lbl = QLabel("مانده حساب: 0 تومان")
        self.bal_lbl.setFont(QFont(FONT_NAME, 13, QFont.Bold))
        h_layout.addWidget(self.bal_lbl)

        layout.addWidget(self.header_card)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #2d3748;
                background-color: #11151a;
            }
            QTabBar::tab {
                background-color: #1a202c;
                color: #a0aec0;
                padding: 10px 15px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #11151a;
                color: #ffffff;
                font-weight: bold;
                border-bottom: 2px solid #319795;
            }
        """)

        self.financial_tab = QWidget()
        f_layout = QVBoxLayout(self.financial_tab)

        toolbar = QHBoxLayout()
        statement_btn = QPushButton("مشاهده صورتحساب کامل")
        statement_btn.setStyleSheet("background-color: #319795; color: white;")
        statement_btn.clicked.connect(self.view_full_statement)
        toolbar.addWidget(statement_btn)
        toolbar.addStretch()
        f_layout.addLayout(toolbar)

        self.tx_table = QTableWidget()
        self.tx_table.setColumnCount(6)
        self.tx_table.setHorizontalHeaderLabels(["ردیف", "تاریخ", "شرح تراکنش", "بدهکار (تومان)", "بستانکار (تومان)", "مانده"])
        self.tx_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tx_table.setStyleSheet("background-color: #1a202c; border: none;")
        f_layout.addWidget(self.tx_table)

        self.tabs.addTab(self.financial_tab, "حساب مالی و تراکنش‌ها")

        self.reports_tab = QWidget()
        r_layout = QVBoxLayout(self.reports_tab)

        self.rep_table = QTableWidget()
        self.rep_table.setColumnCount(4)
        self.rep_table.setHorizontalHeaderLabels(["شماره گزارش", "تاریخ گزارش", "شناسه نمونه", "وضعیت استخراج"])
        self.rep_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.rep_table.setStyleSheet("background-color: #1a202c; border: none;")
        r_layout.addWidget(self.rep_table)

        self.tabs.addTab(self.reports_tab, "گزارش‌های آزمایشگاهی")

        layout.addWidget(self.tabs)

    def set_customer(self, customer_id: int):
        self.customer_id = customer_id
        self.load_profile_data()

    def load_profile_data(self):
        if not self.customer_id:
            return

        with get_db_session() as s:
            cust = s.query(Customer).filter(Customer.id == self.customer_id).first()
            if not cust:
                return

            self.name_lbl.setText(cust.display_name)
            self.code_lbl.setText(f"کد: {cust.customer_code}  |  همراه: {cust.mobile}")

            bal = cust.current_balance or 0.0
            self.bal_lbl.setText(f"مانده حساب: {bal:,.0f} تومان")
            if bal > 0:
                self.bal_lbl.setStyleSheet("color: #e53e3e; font-weight: bold;")
            else:
                self.bal_lbl.setStyleSheet("color: #38a169; font-weight: bold;")

            txs = s.query(FinancialTransaction).filter(FinancialTransaction.customer_id == self.customer_id).order_by(FinancialTransaction.transaction_date.asc()).all()
            self.tx_table.setRowCount(len(txs))
            for idx, tx in enumerate(txs):
                self.tx_table.setItem(idx, 0, QTableWidgetItem(str(idx + 1)))
                self.tx_table.setItem(idx, 1, QTableWidgetItem(tx.transaction_date.strftime("%Y/%m/%d") if tx.transaction_date else ""))
                self.tx_table.setItem(idx, 2, QTableWidgetItem(tx.description or ""))
                self.tx_table.setItem(idx, 3, QTableWidgetItem(f"{tx.debit_amount or 0:,.0f}"))
                self.tx_table.setItem(idx, 4, QTableWidgetItem(f"{tx.credit_amount or 0:,.0f}"))
                self.tx_table.setItem(idx, 5, QTableWidgetItem(f"{tx.running_balance or 0:,.0f}"))

            reps = s.query(LaboratoryReport).filter(LaboratoryReport.customer_id == self.customer_id).all()
            self.rep_table.setRowCount(len(reps))
            for idx, rep in enumerate(reps):
                self.rep_table.setItem(idx, 0, QTableWidgetItem(rep.report_number or "---"))
                self.rep_table.setItem(idx, 1, QTableWidgetItem(rep.test_date or rep.registration_date or "---"))
                self.rep_table.setItem(idx, 2, QTableWidgetItem(rep.sample_id or "---"))
                self.rep_table.setItem(idx, 3, QTableWidgetItem(rep.review_status or "---"))

    def view_full_statement(self):
        if not self.customer_id:
            return
        self.main_window.customer_statement_page.set_customer(self.customer_id)
        self.main_window.navigate_to_page(13)
