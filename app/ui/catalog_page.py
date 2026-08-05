from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QHeaderView, QMessageBox, QFrame, QFormLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from app.config import FONT_NAME
from app.database.session import get_db_session
from app.models.lab_test_catalog import LabTestCatalog
from app.services.catalog_service import CatalogService
from decimal import Decimal

class CatalogPage(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setStyleSheet("background-color: #ffffff;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        header = QHBoxLayout()
        title = QLabel("مدیریت تعرفه و کاتالوگ تست‌های آزمایشگاهی")
        title.setFont(QFont(FONT_NAME, 14, QFont.Bold))
        title.setStyleSheet("color: #a62626; border: none;")
        header.addWidget(title)
        header.addStretch()
        layout.addLayout(header)

        form_card = QFrame()
        form_card.setStyleSheet("background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px;")
        form_layout = QHBoxLayout(form_card)
        form_layout.setContentsMargins(15, 15, 15, 15)

        inner_form = QFormLayout()
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("مثال: TSH, T3, T4")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("نام انگلیسی یا علمی کامل")

        self.unit_input = QLineEdit()
        self.unit_input.setPlaceholderText("مثال: uIU/mL")

        self.range_input = QLineEdit()
        self.range_input.setPlaceholderText("مثال: 0.4 - 4.0")

        self.fee_input = QLineEdit()
        self.fee_input.setPlaceholderText("تعرفه آزمایش به تومان")

        inner_form.addRow("کد اختصاری تست *:", self.code_input)
        inner_form.addRow("نام کامل تست:", self.name_input)
        inner_form.addRow("واحد پیش‌فرض:", self.unit_input)
        inner_form.addRow("محدوده مرجع:", self.range_input)
        inner_form.addRow("هزینه / تعرفه (تومان) *:", self.fee_input)
        form_layout.addLayout(inner_form)

        add_btn = QPushButton("ثبت تست در کاتالوگ")
        add_btn.setStyleSheet("background-color: #a62626; color: white; padding: 12px 20px; font-weight: bold;")
        add_btn.clicked.connect(self.save_test_item)
        form_layout.addWidget(add_btn)

        layout.addWidget(form_card)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["کد تست", "نام تست", "واحد سنجش", "محدوده مرجع", "تعرفه (تومان)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("background-color: #ffffff; border: 1px solid #e0e0e0;")
        layout.addWidget(self.table)

        self.load_catalog()

    def load_catalog(self):
        self.table.setRowCount(0)
        with get_db_session() as s:
            items = s.query(LabTestCatalog).order_by(LabTestCatalog.test_code.asc()).all()
            self.table.setRowCount(len(items))
            for idx, item in enumerate(items):
                self.table.setItem(idx, 0, QTableWidgetItem(item.test_code))
                self.table.setItem(idx, 1, QTableWidgetItem(item.full_name or "---"))
                self.table.setItem(idx, 2, QTableWidgetItem(item.default_unit or "---"))
                self.table.setItem(idx, 3, QTableWidgetItem(item.reference_range or "---"))

                fee_val = item.default_fee or Decimal("0.00")
                self.table.setItem(idx, 4, QTableWidgetItem(f"{fee_val:,.0f}"))

    def save_test_item(self):
        code = self.code_input.text().strip().upper()
        name = self.name_input.text().strip()
        unit = self.unit_input.text().strip()
        ref_range = self.range_input.text().strip()

        if not code:
            QMessageBox.warning(self, "خطا", "لطفاً کد اختصاری تست را وارد کنید.")
            return

        try:
            fee = Decimal(self.fee_input.text().strip() or "0")
        except Exception:
            QMessageBox.warning(self, "خطا", "تعرفه آزمایش باید عددی معتبر باشد.")
            return

        with get_db_session() as s:
            service = CatalogService(s)
            try:
                service.register_test_item(code, name, unit, ref_range, fee)
                QMessageBox.information(self, "موفقیت", f"تست آزمایشگاهی {code} با موفقیت در کاتالوگ ثبت گردید.")
                self.code_input.clear()
                self.name_input.clear()
                self.unit_input.clear()
                self.range_input.clear()
                self.fee_input.clear()
                self.load_catalog()
            except Exception as e:
                QMessageBox.critical(self, "خطا", str(e))
