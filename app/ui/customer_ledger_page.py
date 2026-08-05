from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QHeaderView, QMessageBox, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from app.config import FONT_NAME
from app.database.session import get_db_session
from app.models.customer import Customer

class CustomerLedgerPage(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header Title
        header = QHBoxLayout()
        title = QLabel("حساب مشتریان و دفتر کل مالی")
        title.setFont(QFont(FONT_NAME, 14, QFont.Bold))
        title.setStyleSheet("color: #a62626;")
        header.addWidget(title)
        header.addStretch()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("جستجوی مشتری...")
        self.search_input.setFixedWidth(250)
        self.search_input.textChanged.connect(self.load_ledgers)
        header.addWidget(self.search_input)

        layout.addLayout(header)

        # Table Grid
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "کد مشتری", "نام کامل", "نوع مشتری", "تلفن همراه", "مانده حساب (تومان)", "عملیات صورتحساب"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("background-color: #ffffff; border: 1px solid #e0e0e0;")
        layout.addWidget(self.table)

        self.load_ledgers()

    def load_ledgers(self):
        self.table.setRowCount(0)
        search_query = self.search_input.text().strip()

        with get_db_session() as s:
            query = s.query(Customer).filter(Customer.is_archived == False)
            if search_query:
                query = query.filter(
                    Customer.display_name.like(f"%{search_query}%") |
                    Customer.customer_code.like(f"%{search_query}%")
                )
            custs = query.order_by(Customer.customer_code.asc()).all()
            self.table.setRowCount(len(custs))

            for idx, c in enumerate(custs):
                self.table.setItem(idx, 0, QTableWidgetItem(c.customer_code))
                self.table.setItem(idx, 1, QTableWidgetItem(c.display_name))
                self.table.setItem(idx, 2, QTableWidgetItem(c.customer_type))
                self.table.setItem(idx, 3, QTableWidgetItem(c.mobile or "---"))

                bal = c.current_balance or 0.0
                bal_str = f"{bal:,.0f}"
                bal_item = QTableWidgetItem(bal_str)
                if bal > 0:
                    bal_item.setForeground(Qt.red)
                elif bal < 0:
                    bal_item.setForeground(Qt.green)
                self.table.setItem(idx, 4, bal_item)

                view_btn = QPushButton("مشاهده صورتحساب")
                view_btn.setStyleSheet("background-color: #0284c7; color: white;")
                view_btn.clicked.connect(lambda checked=False, cid=c.id: self.view_statement(cid))
                self.table.setCellWidget(idx, 5, view_btn)

    def view_statement(self, customer_id: int):
        self.main_window.customer_statement_page.set_customer(customer_id)
        self.main_window.navigate_to_page(13)
