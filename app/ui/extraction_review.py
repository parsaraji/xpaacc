from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QHeaderView, QMessageBox, QFrame, QFormLayout, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from app.config import FONT_NAME
from app.database.session import get_db_session
from app.services.report_service import ReportService
from app.services.customer_service import CustomerService
from app.services.accounting_service import AccountingService
from app.models.laboratory_report import LaboratoryReport
from app.models.laboratory_test import LaboratoryTestResult
from app.models.lab_test_catalog import LabTestCatalog
from app.models.customer import Customer
from app.document_processing.confidence import ConfidenceCalculator
from decimal import Decimal
import os

class ExtractionReview(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.extracted_data = {}
        self.total_estimated_fee = Decimal("0.00")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("بازبینی و تایید اطلاعات استخراج شده")
        title.setFont(QFont(FONT_NAME, 14, QFont.Bold))
        layout.addWidget(title)

        # Metrics Panel
        metrics_layout = QHBoxLayout()
        self.conf_lbl = QLabel("میزان اطمینان استخراج: ۱۰۰٪")
        self.conf_lbl.setFont(QFont(FONT_NAME, 11, QFont.Bold))
        self.conf_lbl.setStyleSheet("color: #38a169;")
        metrics_layout.addWidget(self.conf_lbl)

        metrics_layout.addStretch()

        self.fee_lbl = QLabel("جمع هزینه خدمات: ۰ تومان")
        self.fee_lbl.setFont(QFont(FONT_NAME, 11, QFont.Bold))
        self.fee_lbl.setStyleSheet("color: #0284c7;")
        metrics_layout.addWidget(self.fee_lbl)

        layout.addLayout(metrics_layout)

        # 1. Patient form metadata card
        meta_card = QFrame()
        meta_card.setStyleSheet("background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px;")
        meta_layout = QFormLayout(meta_card)
        meta_layout.setContentsMargins(15, 15, 15, 15)

        # Customer Assignment Dropdown
        self.customer_combo = QComboBox()
        self.load_customers_dropdown()

        self.patient_input = QLineEdit()
        self.sample_id_input = QLineEdit()
        self.sample_type_input = QLineEdit()
        self.test_date_input = QLineEdit()

        meta_layout.addRow("اختصاص به مشتری خاص *:", self.customer_combo)
        meta_layout.addRow("نام بیمار (مراجعه‌کننده):", self.patient_input)
        meta_layout.addRow("شناسه نمونه:", self.sample_id_input)
        meta_layout.addRow("نوع نمونه:", self.sample_type_input)
        meta_layout.addRow("تاریخ آزمایش:", self.test_date_input)

        layout.addWidget(meta_card)

        # 2. Results table card
        table_card = QFrame()
        table_card.setStyleSheet("background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px;")
        tc_layout = QVBoxLayout(table_card)

        table_title = QLabel("جدول نتایج آزمایشگاهی ردیابی شده و تعرفه خدمات")
        table_title.setFont(QFont(FONT_NAME, 12, QFont.Bold))
        tc_layout.addWidget(table_title)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["نام تست", "مقدار غلظت", "واحد سنجش", "وضعیت", "تعرفه آزمایش (تومان)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("background-color: #ffffff; border: none;")
        tc_layout.addWidget(self.table)

        layout.addWidget(table_card)

        # Actions Panel
        act_layout = QHBoxLayout()
        confirm_btn = QPushButton("تایید و ثبت نهایی در پرونده و صدور فاکتور")
        confirm_btn.setFont(QFont(FONT_NAME, 11, QFont.Bold))
        confirm_btn.setStyleSheet("background-color: #0284c7; color: white; padding: 10px 24px; border-radius: 4px;")
        confirm_btn.clicked.connect(self.confirm_and_save)
        act_layout.addWidget(confirm_btn)

        cancel_btn = QPushButton("انصراف")
        cancel_btn.clicked.connect(self.cancel_review)
        act_layout.addWidget(cancel_btn)

        act_layout.addStretch()
        layout.addLayout(act_layout)

    def load_customers_dropdown(self):
        self.customer_combo.clear()
        with get_db_session() as s:
            custs = s.query(Customer).filter(Customer.is_archived == False).all()
            for c in custs:
                self.customer_combo.addItem(f"{c.display_name} ({c.customer_code})", c.id)

    def set_review_data(self, data: dict):
        self.extracted_data = data
        self.load_customers_dropdown()

        score = ConfidenceCalculator.calculate_confidence(data)
        self.conf_lbl.setText(f"میزان اطمینان استخراج: {score:.1f}٪")
        if score > 80:
            self.conf_lbl.setStyleSheet("color: #38a169; font-weight: bold;")
        elif score > 50:
            self.conf_lbl.setStyleSheet("color: #dd6b20; font-weight: bold;")
        else:
            self.conf_lbl.setStyleSheet("color: #e53e3e; font-weight: bold;")

        self.patient_input.setText(data.get("patient_name", ""))
        self.sample_id_input.setText(data.get("sample_id", ""))
        self.sample_type_input.setText(data.get("sample_type", ""))
        self.test_date_input.setText(data.get("test_date", ""))

        tests = data.get("tests", [])
        self.table.setRowCount(len(tests))

        self.total_estimated_fee = Decimal("0.00")

        with get_db_session() as s:
            for idx, t in enumerate(tests):
                t_name = t.get("test_name", "")
                val_text = t.get("value", "")
                unit_text = t.get("unit", "")
                status_text = t.get("result_status", "Normal")

                fee = Decimal("0.00")
                catalog_item = s.query(LabTestCatalog).filter(LabTestCatalog.test_code.like(f"%{t_name}%")).first()
                if catalog_item:
                    fee = catalog_item.default_fee or Decimal("0.00")
                    if not unit_text or unit_text == "---":
                        unit_text = catalog_item.default_unit or "---"

                self.total_estimated_fee += fee

                self.table.setItem(idx, 0, QTableWidgetItem(t_name))
                self.table.setItem(idx, 1, QTableWidgetItem(val_text))
                self.table.setItem(idx, 2, QTableWidgetItem(unit_text))
                self.table.setItem(idx, 3, QTableWidgetItem(status_text))
                self.table.setItem(idx, 4, QTableWidgetItem(f"{fee:,.0f}"))

        self.fee_lbl.setText(f"جمع هزینه خدمات: {self.total_estimated_fee:,.0f} تومان")

    def confirm_and_save(self):
        cust_id = self.customer_combo.currentData()
        if not cust_id:
            QMessageBox.warning(self, "خطا", "لطفاً ابتدا مشتری مورد نظر جهت اختصاص آزمایش را انتخاب فرمایید.")
            return

        self.extracted_data["patient_name"] = self.patient_input.text().strip()
        self.extracted_data["sample_id"] = self.sample_id_input.text().strip()
        self.extracted_data["sample_type"] = self.sample_type_input.text().strip()
        self.extracted_data["test_date"] = self.test_date_input.text().strip()

        self.extracted_data["tests"] = []
        for r in range(self.table.rowCount()):
            self.extracted_data["tests"].append({
                "test_name": self.table.item(r, 0).text() if self.table.item(r, 0) else "",
                "value": self.table.item(r, 1).text() if self.table.item(r, 1) else "",
                "unit": self.table.item(r, 2).text() if self.table.item(r, 2) else "",
                "result_status": self.table.item(r, 3).text() if self.table.item(r, 3) else "Normal",
                "fee": Decimal(self.table.item(r, 4).text().replace(",", "") if self.table.item(r, 4) else "0")
            })

        with get_db_session() as s:
            try:
                report_service = ReportService(s)
                rep_num = f"REP-{(s.query(LaboratoryReport).count() + 9001):04d}"

                rep_data = {
                    "report_number": rep_num,
                    "customer_id": cust_id,
                    "patient_name": self.extracted_data["patient_name"],
                    "sample_id": self.extracted_data["sample_id"],
                    "sample_type": self.extracted_data["sample_type"],
                    "test_date": self.extracted_data["test_date"],
                    "original_filename": self.extracted_data.get("original_filename", "imported_doc.xps")
                }

                report = report_service.register_report(rep_data)

                # Save structured results
                for tr in self.extracted_data["tests"]:
                    db_tr = LaboratoryTestResult(
                        report_id=report.id,
                        test_name=tr["test_name"],
                        value_text=tr["value"],
                        unit=tr["unit"],
                        result_status=tr["result_status"]
                    )
                    s.add(db_tr)
                s.flush()

                # Issue invoice charge on customer
                if self.total_estimated_fee > 0:
                    accounting_service = AccountingService(s)
                    accounting_service.post_transaction(
                        customer_id=cust_id,
                        transaction_type="Laboratory service charge",
                        debit_amount=self.total_estimated_fee,
                        credit_amount=Decimal("0.00"),
                        description=f"هزینه خدمات آزمایشگاه گزارش شماره {rep_num}",
                        report_id=report.id
                    )

                QMessageBox.information(
                    self, "موفقیت",
                    f"سند آزمایشگاهی بیمار {report.patient_name} با موفقیت ثبت و به حساب مشتری انتخابی به مبلغ {self.total_estimated_fee:,.0f} تومان منظور گردید."
                )

                self.main_window.reports_page.load_reports()
                self.main_window.navigate_to_page(3)
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در ثبت اطلاعات: {str(e)}")

    def cancel_review(self):
        self.main_window.navigate_to_page(4)
