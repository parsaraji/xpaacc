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
from app.models.laboratory_test import LaboratoryTestResult

class CustomerProfile(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.customer_id = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 1. Profile Header block
        self.header_card = QFrame()
        self.header_card.setStyleSheet("background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px;")
        h_layout = QHBoxLayout(self.header_card)
        h_layout.setContentsMargins(15, 15, 15, 15)

        self.name_lbl = QLabel("نام مشتری")
        self.name_lbl.setFont(QFont(FONT_NAME, 14, QFont.Bold))
        self.name_lbl.setStyleSheet("color: #0284c7;")
        h_layout.addWidget(self.name_lbl)

        self.code_lbl = QLabel("کد مشتری")
        self.code_lbl.setFont(QFont(FONT_NAME, 11))
        self.code_lbl.setStyleSheet("color: #4b5563;")
        h_layout.addWidget(self.code_lbl)

        h_layout.addStretch()

        self.bal_lbl = QLabel("مانده حساب: 0 تومان")
        self.bal_lbl.setFont(QFont(FONT_NAME, 13, QFont.Bold))
        h_layout.addWidget(self.bal_lbl)

        layout.addWidget(self.header_card)

        # 2. Main Tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #e5e7eb;
                background-color: #ffffff;
            }
            QTabBar::tab {
                background-color: #f3f4f6;
                color: #4b5563;
                padding: 10px 15px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                color: #0284c7;
                font-weight: bold;
                border-bottom: 2px solid #0284c7;
            }
        """)

        # Tab 1: Financial Statement List
        self.financial_tab = QWidget()
        f_layout = QVBoxLayout(self.financial_tab)

        # Toolbar actions
        toolbar = QHBoxLayout()
        statement_btn = QPushButton("مشاهده صورتحساب کامل")
        statement_btn.setStyleSheet("background-color: #0284c7; color: white;")
        statement_btn.clicked.connect(self.view_full_statement)
        toolbar.addWidget(statement_btn)
        toolbar.addStretch()
        f_layout.addLayout(toolbar)

        self.tx_table = QTableWidget()
        self.tx_table.setColumnCount(6)
        self.tx_table.setHorizontalHeaderLabels(["ردیف", "تاریخ", "شرح تراکنش", "بدهکار (تومان)", "بستانکار (تومان)", "مانده"])
        self.tx_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tx_table.setStyleSheet("background-color: #ffffff; border: none;")
        f_layout.addWidget(self.tx_table)

        self.tabs.addTab(self.financial_tab, "حساب مالی و تراکنش‌ها")

        # Tab 2: Reports & Tests Lookup List
        self.reports_tab = QWidget()
        r_layout = QVBoxLayout(self.reports_tab)

        split_layout = QHBoxLayout()
        split_layout.setSpacing(15)

        # Left Column: Reports List
        reports_subframe = QFrame()
        reports_subframe_layout = QVBoxLayout(reports_subframe)
        reports_subframe_layout.setContentsMargins(0, 0, 0, 0)

        rep_lbl = QLabel("آزمایش‌های ثبت شده (جهت مشاهده جزئیات روی ردیف کلیک کنید)")
        rep_lbl.setFont(QFont(FONT_NAME, 10, QFont.Bold))
        reports_subframe_layout.addWidget(rep_lbl)

        self.rep_table = QTableWidget()
        self.rep_table.setColumnCount(4)
        self.rep_table.setHorizontalHeaderLabels(["شماره گزارش", "تاریخ گزارش", "شناسه نمونه", "وضعیت استخراج"])
        self.rep_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.rep_table.setStyleSheet("background-color: #ffffff; border: 1px solid #e5e7eb;")
        self.rep_table.itemSelectionChanged.connect(self.on_report_selection_changed)
        reports_subframe_layout.addWidget(self.rep_table)

        split_layout.addWidget(reports_subframe, stretch=1)

        # Right Column: Detailed test items grid
        details_subframe = QFrame()
        details_subframe.setStyleSheet("background-color: #f9fafb; border: 1px solid #e5e7eb; border-radius: 6px;")
        details_layout = QVBoxLayout(details_subframe)
        details_layout.setContentsMargins(10, 10, 10, 10)

        details_lbl = QLabel("جزئیات آیتم‌ها و پارامترهای آزمایشگاهی")
        details_lbl.setFont(QFont(FONT_NAME, 10, QFont.Bold))
        details_lbl.setStyleSheet("color: #0284c7;")
        details_layout.addWidget(details_lbl)

        self.details_table = QTableWidget()
        self.details_table.setColumnCount(4)
        self.details_table.setHorizontalHeaderLabels(["نام تست", "نتیجه سنجش", "واحد", "وضعیت"])
        self.details_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.details_table.setStyleSheet("background-color: #ffffff;")
        details_layout.addWidget(self.details_table)

        split_layout.addWidget(details_subframe, stretch=1)

        r_layout.addLayout(split_layout)
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
                self.bal_lbl.setStyleSheet("color: #ef4444; font-weight: bold;")
            else:
                self.bal_lbl.setStyleSheet("color: #10b981; font-weight: bold;")

            txs = s.query(FinancialTransaction).filter(FinancialTransaction.customer_id == self.customer_id).order_by(FinancialTransaction.transaction_date.asc()).all()
            self.tx_table.setRowCount(len(txs))
            for idx, tx in enumerate(txs):
                self.tx_table.setItem(idx, 0, QTableWidgetItem(str(idx + 1)))
                self.tx_table.setItem(idx, 1, QTableWidgetItem(tx.transaction_date.strftime("%Y/%m/%d") if tx.transaction_date else ""))
                self.tx_table.setItem(idx, 2, QTableWidgetItem(tx.description or ""))
                self.tx_table.setItem(idx, 3, QTableWidgetItem(f"{tx.debit_amount or 0:,.0f}"))
                self.tx_table.setItem(idx, 4, QTableWidgetItem(f"{tx.credit_amount or 0:,.0f}"))
                self.tx_table.setItem(idx, 5, QTableWidgetItem(f"{tx.running_balance or 0:,.0f}"))

            # Populate Reports list with internal custom ID tagging
            reps = s.query(LaboratoryReport).filter(LaboratoryReport.customer_id == self.customer_id).all()
            self.rep_table.setRowCount(len(reps))
            for idx, rep in enumerate(reps):
                item_rep_num = QTableWidgetItem(rep.report_number or "---")
                item_rep_num.setData(Qt.UserRole, rep.id) # Embed Database report ID in the item metadata

                self.rep_table.setItem(idx, 0, item_rep_num)
                self.rep_table.setItem(idx, 1, QTableWidgetItem(rep.test_date or rep.registration_date or "---"))
                self.rep_table.setItem(idx, 2, QTableWidgetItem(rep.sample_id or "---"))
                self.rep_table.setItem(idx, 3, QTableWidgetItem(rep.review_status or "---"))

    def on_report_selection_changed(self):
        self.details_table.setRowCount(0)
        selected_ranges = self.rep_table.selectedRanges()
        if not selected_ranges:
            return

        row = selected_ranges[0].topRow()
        item = self.rep_table.item(row, 0)
        if not item:
            return

        report_id = item.data(Qt.UserRole)
        if not report_id:
            return

        with get_db_session() as s:
            tests = s.query(LaboratoryTestResult).filter(LaboratoryTestResult.report_id == report_id).all()
            self.details_table.setRowCount(len(tests))
            for idx, t in enumerate(tests):
                self.details_table.setItem(idx, 0, QTableWidgetItem(t.test_name))
                self.details_table.setItem(idx, 1, QTableWidgetItem(t.value_text or "---"))
                self.details_table.setItem(idx, 2, QTableWidgetItem(t.unit or "---"))
                self.details_table.setItem(idx, 3, QTableWidgetItem(t.result_status or "Normal"))

    def view_full_statement(self):
        if not self.customer_id:
            return
        self.main_window.customer_statement_page.set_customer(self.customer_id)
        self.main_window.navigate_to_page(13)
