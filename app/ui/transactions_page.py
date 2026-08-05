from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QHeaderView, QMessageBox, QFrame, QFormLayout, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from app.config import FONT_NAME
from app.database.session import get_db_session
from app.models.customer import Customer
from app.models.transaction import FinancialTransaction
from app.services.accounting_service import AccountingService
from decimal import Decimal

class TransactionsPage(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("دریافت‌ها، پرداخت‌ها و تراکنش‌های مالی")
        title.setFont(QFont(FONT_NAME, 14, QFont.Bold))
        layout.addWidget(title)

        # Form to add custom debit/credit
        form_card = QFrame()
        form_card.setStyleSheet("background-color: #1a202c; border: 1px solid #2d3748; border-radius: 8px;")
        form_layout = QHBoxLayout(form_card)
        form_layout.setContentsMargins(15, 15, 15, 15)

        inner_form = QFormLayout()
        self.cust_combo = QComboBox()
        self.load_customers_combo()

        self.type_combo = QComboBox()
        self.type_combo.addItems(["Customer payment received", "Debit transaction", "Credit transaction", "Discount"])

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("مبلغ به تومان")

        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("توضیحات تراکنش")

        inner_form.addRow("انتخاب مشتری:", self.cust_combo)
        inner_form.addRow("نوع تراکنش:", self.type_combo)
        inner_form.addRow("مبلغ تراکنش:", self.amount_input)
        inner_form.addRow("شرح بابت:", self.desc_input)
        form_layout.addLayout(inner_form)

        submit_btn = QPushButton("ثبت تراکنش مالی")
        submit_btn.setStyleSheet("background-color: #319795; color: white; padding: 12px 20px; font-weight: bold;")
        submit_btn.clicked.connect(self.save_transaction)
        form_layout.addWidget(submit_btn)

        layout.addWidget(form_card)

        # Transactions List
        list_title = QLabel("لیست آخرین تراکنش‌های ثبت شده در سیستم")
        list_title.setFont(QFont(FONT_NAME, 11, QFont.Bold))
        layout.addWidget(list_title)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["شماره سند", "نام مشتری", "نوع تراکنش", "بدهکار", "بستانکار", "تاریخ ثبت"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("background-color: #1a202c; border: 1px solid #2d3748;")
        layout.addWidget(self.table)

        self.load_transactions()

    def load_customers_combo(self):
        self.cust_combo.clear()
        with get_db_session() as s:
            custs = s.query(Customer).filter(Customer.is_archived == False).all()
            for c in custs:
                self.cust_combo.addItem(c.display_name, c.id)

    def load_transactions(self):
        self.table.setRowCount(0)
        with get_db_session() as s:
            txs = s.query(FinancialTransaction).order_by(FinancialTransaction.id.desc()).limit(20).all()
            self.table.setRowCount(len(txs))
            for idx, tx in enumerate(txs):
                self.table.setItem(idx, 0, QTableWidgetItem(tx.transaction_number))
                self.table.setItem(idx, 1, QTableWidgetItem(tx.customer.display_name if tx.customer else "---"))
                self.table.setItem(idx, 2, QTableWidgetItem(tx.transaction_type))
                self.table.setItem(idx, 3, QTableWidgetItem(f"{tx.debit_amount or 0:,.0f}"))
                self.table.setItem(idx, 4, QTableWidgetItem(f"{tx.credit_amount or 0:,.0f}"))
                self.table.setItem(idx, 5, QTableWidgetItem(tx.transaction_date.strftime("%Y/%m/%d %H:%M:%S") if tx.transaction_date else ""))

    def save_transaction(self):
        cust_id = self.cust_combo.currentData()
        if not cust_id:
            QMessageBox.warning(self, "خطا", "لطفاً ابتدا یک مشتری انتخاب کنید.")
            return

        try:
            amt = Decimal(self.amount_input.text().strip() or "0")
        except Exception:
            QMessageBox.warning(self, "خطا", "مبلغ باید عددی معتبر باشد.")
            return

        if amt <= 0:
            QMessageBox.warning(self, "خطا", "مبلغ باید بزرگتر از صفر باشد.")
            return

        tx_type = self.type_combo.currentText()
        deb = Decimal("0.00")
        cred = Decimal("0.00")

        if tx_type in ["Debit transaction"]:
            deb = amt
        else:
            cred = amt

        with get_db_session() as s:
            service = AccountingService(s)
            try:
                service.post_transaction(
                    customer_id=cust_id,
                    transaction_type=tx_type,
                    debit_amount=deb,
                    credit_amount=cred,
                    description=self.desc_input.text().strip() or f"ثبت دستی {tx_type}"
                )
                QMessageBox.information(self, "موفقیت", "تراکنش مالی با موفقیت ثبت شد.")
                self.amount_input.clear()
                self.desc_input.clear()
                self.load_transactions()
                self.main_window.dashboard_page.load_dashboard_summaries()
            except Exception as e:
                QMessageBox.critical(self, "خطا", str(e))
