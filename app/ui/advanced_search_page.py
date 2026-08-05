from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QFormLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from app.config import FONT_NAME
from app.database.session import get_db_session
from app.models.laboratory_report import LaboratoryReport
from app.models.laboratory_test import LaboratoryTestResult

class AdvancedSearchPage(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setStyleSheet("background-color: #ffffff;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("جستجوی پیشرفته اسناد، بیماران و سوابق آزمایشگاهی")
        title.setFont(QFont(FONT_NAME, 14, QFont.Bold))
        title.setStyleSheet("color: #a62626; border: none;")
        layout.addWidget(title)

        filter_card = QFrame()
        filter_card.setStyleSheet("background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px;")
        filter_layout = QFormLayout(filter_card)
        filter_layout.setContentsMargins(15, 15, 15, 15)

        self.patient_search = QLineEdit()
        self.patient_search.setPlaceholderText("نام بیمار یا مشتری")

        self.test_search = QLineEdit()
        self.test_search.setPlaceholderText("کد یا نام تست آزمایشگاهی (مانند TSH یا SGPT)")

        self.sample_id_search = QLineEdit()
        self.sample_id_search.setPlaceholderText("شناسه نمونه آزمایشگاهی")

        filter_layout.addRow("نام بیمار / مشتری:", self.patient_search)
        filter_layout.addRow("تست آزمایشگاهی:", self.test_search)
        filter_layout.addRow("شناسه نمونه:", self.sample_id_search)

        btn_layout = QHBoxLayout()
        search_btn = QPushButton("شروع جستجوی پیشرفته")
        search_btn.setStyleSheet("background-color: #a62626; color: white; padding: 8px 16px; font-weight: bold;")
        search_btn.clicked.connect(self.run_search)
        btn_layout.addWidget(search_btn)

        filter_layout.addRow("", btn_layout)
        layout.addWidget(filter_card)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["شماره گزارش", "نام بیمار / مشتری", "شناسه نمونه", "تاریخ ثبت", "وضعیت"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("background-color: #ffffff; border: 1px solid #e0e0e0;")
        layout.addWidget(self.table)

    def run_search(self):
        self.table.setRowCount(0)
        p_name = self.patient_search.text().strip()
        t_name = self.test_search.text().strip()
        s_id = self.sample_id_search.text().strip()

        with get_db_session() as s:
            query = s.query(LaboratoryReport)
            if p_name:
                query = query.filter(LaboratoryReport.patient_name.like(f"%{p_name}%"))
            if s_id:
                query = query.filter(LaboratoryReport.sample_id.like(f"%{s_id}%"))

            if t_name:
                # Explicit clean join on results relationship
                query = query.join(LaboratoryReport.results).filter(LaboratoryTestResult.test_name.like(f"%{t_name}%"))

            results = query.distinct().order_by(LaboratoryReport.id.desc()).all()
            self.table.setRowCount(len(results))

            for idx, r in enumerate(results):
                self.table.setItem(idx, 0, QTableWidgetItem(r.report_number or "---"))
                self.table.setItem(idx, 1, QTableWidgetItem(r.patient_name or "---"))
                self.table.setItem(idx, 2, QTableWidgetItem(r.sample_id or "---"))
                self.table.setItem(idx, 3, QTableWidgetItem(r.test_date or "---"))
                self.table.setItem(idx, 4, QTableWidgetItem(r.review_status or "جدید"))
