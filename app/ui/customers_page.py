from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QHeaderView, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from app.config import FONT_NAME
from app.database.session import get_db_session
from app.models.customer import Customer

class CustomersPage(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        header = QHBoxLayout()
        title = QLabel("مدیریت مشتریان و همکاران")
        title.setFont(QFont(FONT_NAME, 14, QFont.Bold))
        header.addWidget(title)
        header.addStretch()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("جستجو بر اساس نام، موبایل، یا کد مشتری...")
        self.search_input.setFixedWidth(300)
        self.search_input.textChanged.connect(self.load_customers)
        header.addWidget(self.search_input)

        add_btn = QPushButton("افزودن مشتری جدید")
        add_btn.setFont(QFont(FONT_NAME, 10, QFont.Bold))
        add_btn.setStyleSheet("background-color: #319795; color: white; padding: 6px 12px; border-radius: 4px;")
        add_btn.clicked.connect(lambda: self.main_window.navigate_to_page(2))
        header.addWidget(add_btn)

        layout.addLayout(header)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "کد مشتری", "نام / شرکت", "نوع مشتری", "تلفن همراه", "استان / شهر", "مانده حساب (تومان)", "عملیات"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #1a202c;
                gridline-color: #2d3748;
                border: 1px solid #2d3748;
            }
            QHeaderView::section {
                background-color: #2d3748;
                color: #e2e8f0;
                padding: 6px;
                font-weight: bold;
                border: 1px solid #2d3748;
            }
        """)
        layout.addWidget(self.table)

        self.load_customers()

    def load_customers(self):
        self.table.setRowCount(0)
        search_query = self.search_input.text().strip()

        with get_db_session() as s:
            query = s.query(Customer).filter(Customer.is_archived == False)
            if search_query:
                query = query.filter(
                    Customer.display_name.like(f"%{search_query}%") |
                    Customer.mobile.like(f"%{search_query}%") |
                    Customer.customer_code.like(f"%{search_query}%")
                )

            customers = query.order_by(Customer.customer_code.asc()).all()
            self.table.setRowCount(len(customers))

            for idx, cust in enumerate(customers):
                self.table.setItem(idx, 0, QTableWidgetItem(cust.customer_code))
                self.table.setItem(idx, 1, QTableWidgetItem(cust.display_name))
                self.table.setItem(idx, 2, QTableWidgetItem(cust.customer_type))
                self.table.setItem(idx, 3, QTableWidgetItem(cust.mobile))
                self.table.setItem(idx, 4, QTableWidgetItem(f"{cust.province or ''} - {cust.city or ''}"))

                bal = cust.current_balance or 0.0
                bal_str = f"{bal:,.0f}"
                bal_item = QTableWidgetItem(bal_str)
                if bal > 0:
                    bal_item.setForeground(Qt.red)
                elif bal < 0:
                    bal_item.setForeground(Qt.green)
                self.table.setItem(idx, 5, bal_item)

                view_btn = QPushButton("مشاهده پرونده")
                view_btn.setStyleSheet("background-color: #2d3748; color: white; border-radius: 3px; max-width: 100px;")
                view_btn.clicked.connect(lambda checked=False, cid=cust.id: self.view_customer_profile(cid))
                self.table.setCellWidget(idx, 6, view_btn)

    def view_customer_profile(self, customer_id: int):
        self.main_window.customer_profile_page.set_customer(customer_id)
        self.main_window.navigate_to_page(12)
