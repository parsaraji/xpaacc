from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QFormLayout, QTextEdit, QMessageBox, QFrame, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from app.config import FONT_NAME
from app.database.session import get_db_session
from app.services.customer_service import CustomerService
from decimal import Decimal

class CustomerForm(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        scroll.setWidget(self.scroll_widget)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

        layout = QVBoxLayout(self.scroll_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel("ثبت و افزودن مشتری جدید")
        title.setFont(QFont(FONT_NAME, 14, QFont.Bold))
        layout.addWidget(title)

        card = QFrame()
        card.setStyleSheet("background-color: #1a202c; border: 1px solid #2d3748; border-radius: 8px;")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(15, 15, 15, 15)

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignRight)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("نام کامل یا نام شرکت")

        self.type_combo = QComboBox()
        self.type_combo.addItems(["شخص حقیقی", "شخص حقوقی", "دامپزشک", "کلینیک", "آزمایشگاه", "پت‌شاپ", "پرورش‌دهنده"])

        self.mobile_input = QLineEdit()
        self.mobile_input.setPlaceholderText("مثال: 09121234567")

        self.national_id_input = QLineEdit()
        self.national_id_input.setPlaceholderText("کد ملی یا شناسه ملی حقوقی")

        self.province_input = QLineEdit()
        self.city_input = QLineEdit()
        self.address_input = QLineEdit()

        self.credit_limit_input = QLineEdit("0")
        self.opening_bal_input = QLineEdit("0")
        self.opening_type_combo = QComboBox()
        self.opening_type_combo.addItems(["بدهکار (DEBIT)", "بستانکار (CREDIT)", "بدون حساب (NONE)"])

        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(80)

        form.addRow("نام کامل / نام شرکت *:", self.name_input)
        form.addRow("نوع مشتری:", self.type_combo)
        form.addRow("تلفن همراه *:", self.mobile_input)
        form.addRow("شناسه ملی / کد ملی:", self.national_id_input)
        form.addRow("استان:", self.province_input)
        form.addRow("شهر:", self.city_input)
        form.addRow("آدرس کامل:", self.address_input)
        form.addRow("سقف اعتبار مالی (تومان):", self.credit_limit_input)
        form.addRow("مانده حساب اولیه (تومان):", self.opening_bal_input)
        form.addRow("نوع مانده حساب اولیه:", self.opening_type_combo)
        form.addRow("یادداشت‌ها:", self.notes_input)

        card_layout.addLayout(form)
        layout.addWidget(card)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("ذخیره مشتری")
        save_btn.setFont(QFont(FONT_NAME, 11, QFont.Bold))
        save_btn.setStyleSheet("background-color: #319795; color: white; padding: 10px 24px; border-radius: 4px;")
        save_btn.clicked.connect(self.save_customer)
        btn_layout.addWidget(save_btn)

        clear_btn = QPushButton("پاک کردن فرم")
        clear_btn.setStyleSheet("background-color: #4a5568; color: white; padding: 10px 18px; border-radius: 4px;")
        clear_btn.clicked.connect(self.clear_form)
        btn_layout.addWidget(clear_btn)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)

    def save_customer(self):
        name = self.name_input.text().strip()
        mobile = self.mobile_input.text().strip()

        if not name or not mobile:
            QMessageBox.warning(self, "خطا در ثبت اطلاعات", "تکمیل فیلدهای ستاره‌دار الزامی است.")
            return

        try:
            cred_limit = Decimal(self.credit_limit_input.text().strip() or "0")
            open_bal = Decimal(self.opening_bal_input.text().strip() or "0")
        except Exception:
            QMessageBox.warning(self, "خطا", "سقف اعتبار و مانده حساب اولیه باید عددی باشند.")
            return

        sel_type = self.opening_type_combo.currentText()
        bal_type = "NONE"
        if "DEBIT" in sel_type:
            bal_type = "DEBIT"
        elif "CREDIT" in sel_type:
            bal_type = "CREDIT"

        cust_data = {
            "customer_type": self.type_combo.currentText(),
            "display_name": name,
            "mobile": mobile,
            "national_id": self.national_id_input.text().strip() or None,
            "province": self.province_input.text().strip() or None,
            "city": self.city_input.text().strip() or None,
            "address": self.address_input.text().strip() or None,
            "credit_limit": cred_limit,
            "opening_balance": open_bal,
            "opening_balance_type": bal_type
        }

        with get_db_session() as s:
            service = CustomerService(s)
            try:
                cust = service.create_customer(cust_data)
                QMessageBox.information(self, "موفقیت", f"مشتری {cust.display_name} با کد {cust.customer_code} ثبت گردید.")
                self.clear_form()
                self.main_window.customers_page.load_customers()
                self.main_window.navigate_to_page(1)
            except Exception as e:
                QMessageBox.critical(self, "خطا در پایگاه داده", str(e))

    def clear_form(self):
        self.name_input.clear()
        self.mobile_input.clear()
        self.national_id_input.clear()
        self.province_input.clear()
        self.city_input.clear()
        self.address_input.clear()
        self.credit_limit_input.setText("0")
        self.opening_bal_input.setText("0")
        self.notes_input.clear()
