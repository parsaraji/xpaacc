from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton, QComboBox, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from app.config import FONT_NAME
from app.database.session import get_db_session
from app.models.customer import Customer
from app.models.transaction import FinancialTransaction
from app.reports.excel_exporter import ExcelExporter
import os

class CustomerStatement(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.customer_id = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        header = QHBoxLayout()
        self.title_lbl = QLabel("صورتحساب مالی مشتری")
        self.title_lbl.setFont(QFont(FONT_NAME, 14, QFont.Bold))
        header.addWidget(self.title_lbl)
        header.addStretch()

        excel_btn = QPushButton("خروجی اکسل")
        excel_btn.setStyleSheet("background-color: #2f855a; color: white; padding: 6px 12px;")
        excel_btn.clicked.connect(self.export_to_excel)
        header.addWidget(excel_btn)

        layout.addLayout(header)

        self.summary_frame = QFrame()
        self.summary_frame.setStyleSheet("background-color: #1a202c; border: 1px solid #2d3748; border-radius: 8px;")
        sf_layout = QHBoxLayout(self.summary_frame)
        sf_layout.setContentsMargins(15, 15, 15, 15)

        self.totals_lbl = QLabel("جمع بدهکار: 0 | جمع بستانکار: 0 | مانده نهایی: 0")
        self.totals_lbl.setFont(QFont(FONT_NAME, 11, QFont.Bold))
        sf_layout.addWidget(self.totals_lbl)
        sf_layout.addStretch()

        layout.addWidget(self.summary_frame)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ردیف", "تاریخ", "شماره سند", "نوع تراکنش", "شرح تراکنش", "بدهکار (تومان)", "بستانکار (تومان)"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("background-color: #1a202c; border: 1px solid #2d3748;")
        layout.addWidget(self.table)

    def set_customer(self, customer_id: int):
        self.customer_id = customer_id
        self.load_statement()

    def load_statement(self):
        if not self.customer_id:
            return

        with get_db_session() as s:
            cust = s.query(Customer).filter(Customer.id == self.customer_id).first()
            if not cust:
                return

            self.title_lbl.setText(f"صورتحساب مالی - {cust.display_name} ({cust.customer_code})")

            txs = s.query(FinancialTransaction).filter(FinancialTransaction.customer_id == self.customer_id).order_by(FinancialTransaction.transaction_date.asc()).all()
            self.table.setRowCount(len(txs))

            tot_debit = 0
            tot_credit = 0

            for idx, tx in enumerate(txs):
                deb = tx.debit_amount or 0
                cred = tx.credit_amount or 0
                tot_debit += deb
                tot_credit += cred

                self.table.setItem(idx, 0, QTableWidgetItem(str(idx + 1)))
                self.table.setItem(idx, 1, QTableWidgetItem(tx.transaction_date.strftime("%Y/%m/%d") if tx.transaction_date else ""))
                self.table.setItem(idx, 2, QTableWidgetItem(tx.transaction_number))
                self.table.setItem(idx, 3, QTableWidgetItem(tx.transaction_type))
                self.table.setItem(idx, 4, QTableWidgetItem(tx.description or ""))
                self.table.setItem(idx, 5, QTableWidgetItem(f"{deb:,.0f}"))
                self.table.setItem(idx, 6, QTableWidgetItem(f"{cred:,.0f}"))

            bal = cust.current_balance or 0.0
            self.totals_lbl.setText(f"جمع کل بدهکار: {tot_debit:,.0f} تومان  |  جمع کل بستانکار: {tot_credit:,.0f} تومان  |  مانده نهایی: {bal:,.0f} تومان")

    def export_to_excel(self):
        if not self.customer_id:
            return

        try:
            with get_db_session() as s:
                txs = s.query(FinancialTransaction).filter(FinancialTransaction.customer_id == self.customer_id).all()
                if not txs:
                    QMessageBox.warning(self, "خطا", "تراکنشی برای این مشتری یافت نشد.")
                    return

                os.makedirs("documents", exist_ok=True)
                dest = "documents/customer_statement.xlsx"

                exporter = ExcelExporter()
                exporter.export_transactions(txs, dest)
                QMessageBox.information(self, "موفقیت", f"خروجی اکسل با موفقیت در مسیر زیر ذخیره گردید:\n{dest}")
        except Exception as e:
            QMessageBox.critical(self, "خطا", str(e))
