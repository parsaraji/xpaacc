from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QHeaderView, QMessageBox, QDialog, QFormLayout, QComboBox, QDialogButtonBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from app.config import FONT_NAME
from app.database.session import get_db_session
from app.models.customer import Customer
from app.services.customer_service import CustomerService

class EditCustomerDialog(QDialog):
    def __init__(self, customer_id: int, parent=None):
        super().__init__(parent)
        self.customer_id = customer_id
        self.setWindowTitle("ویرایش اطلاعات مشتری")
        self.setMinimumSize(450, 350)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        form = QFormLayout()
        self.name_input = QLineEdit()
        self.type_combo = QComboBox()
        self.type_combo.addItems(["شخص حقیقی", "شخص حقوقی", "دامپزشک", "کلینیک", "آزمایشگاه", "پت‌شاپ", "پرورش‌دهنده"])

        self.mobile_input = QLineEdit()
        self.national_id_input = QLineEdit()
        self.province_input = QLineEdit()
        self.city_input = QLineEdit()
        self.address_input = QLineEdit()

        form.addRow("نام کامل / شرکت *:", self.name_input)
        form.addRow("نوع مشتری:", self.type_combo)
        form.addRow("تلفن همراه *:", self.mobile_input)
        form.addRow("کد ملی / شناسه:", self.national_id_input)
        form.addRow("استان:", self.province_input)
        form.addRow("شهر:", self.city_input)
        form.addRow("آدرس کامل:", self.address_input)
        layout.addLayout(form)

        # OK / Cancel Buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, parent=self)
        self.buttons.accepted.connect(self.save_data)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

        self.load_data()

    def load_data(self):
        with get_db_session() as s:
            cust = s.query(Customer).filter(Customer.id == self.customer_id).first()
            if cust:
                self.name_input.setText(cust.display_name)
                self.type_combo.setCurrentText(cust.customer_type)
                self.mobile_input.setText(cust.mobile or "")
                self.national_id_input.setText(cust.national_id or "")
                self.province_input.setText(cust.province or "")
                self.city_input.setText(cust.city or "")
                self.address_input.setText(cust.address or "")

    def save_data(self):
        name = self.name_input.text().strip()
        mobile = self.mobile_input.text().strip()

        if not name or not mobile:
            QMessageBox.warning(self, "خطا", "تکمیل فیلدهای ستاره‌دار الزامی است.")
            return

        with get_db_session() as s:
            cust = s.query(Customer).filter(Customer.id == self.customer_id).first()
            if cust:
                cust.display_name = name
                cust.customer_type = self.type_combo.currentText()
                cust.mobile = mobile
                cust.national_id = self.national_id_input.text().strip() or None
                cust.province = self.province_input.text().strip() or None
                cust.city = self.city_input.text().strip() or None
                cust.address = self.address_input.text().strip() or None
                s.flush()

        self.accept()


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
        add_btn.setStyleSheet("background-color: #a62626; color: white; padding: 6px 12px; border-radius: 4px;")
        add_btn.clicked.connect(lambda: self.main_window.navigate_to_page(2))
        header.addWidget(add_btn)

        layout.addLayout(header)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "کد مشتری", "نام / شرکت", "نوع مشتری", "تلفن همراه", "استان / شهر", "مانده حساب (تومان)", "عملیات کاربردی"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                gridline-color: #e5e7eb;
                border: 1px solid #e5e7eb;
            }
            QHeaderView::section {
                background-color: #f3f4f6;
                color: #374151;
                padding: 6px;
                font-weight: bold;
                border: 1px solid #e5e7eb;
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

                # Operations panel widget
                widget = QWidget()
                w_layout = QHBoxLayout(widget)
                w_layout.setContentsMargins(4, 4, 4, 4)
                w_layout.setSpacing(4)

                view_btn = QPushButton("پرونده")
                view_btn.setStyleSheet("background-color: #0284c7; color: white;")
                view_btn.clicked.connect(lambda checked=False, cid=cust.id: self.view_customer_profile(cid))
                w_layout.addWidget(view_btn)

                edit_btn = QPushButton("ویرایش")
                edit_btn.setStyleSheet("background-color: #f59e0b; color: white;")
                edit_btn.clicked.connect(lambda checked=False, cid=cust.id: self.edit_customer_record(cid))
                w_layout.addWidget(edit_btn)

                del_btn = QPushButton("حذف")
                del_btn.setStyleSheet("background-color: #ef4444; color: white;")
                del_btn.clicked.connect(lambda checked=False, cid=cust.id: self.delete_customer_record(cid))
                w_layout.addWidget(del_btn)

                self.table.setCellWidget(idx, 6, widget)

    def view_customer_profile(self, customer_id: int):
        self.main_window.customer_profile_page.set_customer(customer_id)
        self.main_window.navigate_to_page(12)

    def edit_customer_record(self, customer_id: int):
        dialog = EditCustomerDialog(customer_id, self)
        if dialog.exec() == QDialog.Accepted:
            QMessageBox.information(self, "موفقیت", "اطلاعات مشتری با موفقیت اصلاح گردید.")
            self.load_customers()

    def delete_customer_record(self, customer_id: int):
        reply = QMessageBox.question(self, "تأیید حذف", "آیا از حذف این مشتری و بایگانی پرونده او مطمئن هستید؟", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            with get_db_session() as s:
                cust = s.query(Customer).filter(Customer.id == customer_id).first()
                if cust:
                    cust.is_archived = True
                    s.flush()
                    QMessageBox.information(self, "موفقیت", "پرونده مشتری با موفقیت بایگانی/حذف گردید.")
                    self.load_customers()
