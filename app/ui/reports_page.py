from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QLineEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from app.config import FONT_NAME
from app.database.session import get_db_session
from app.models.laboratory_report import LaboratoryReport

class ReportsPage(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        header = QHBoxLayout()
        title = QLabel("بایگانی گزارش‌های آزمایشگاهی")
        title.setFont(QFont(FONT_NAME, 14, QFont.Bold))
        header.addWidget(title)
        header.addStretch()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("جستجو بر اساس نام بیمار یا شناسه نمونه...")
        self.search_input.setFixedWidth(260)
        self.search_input.textChanged.connect(self.load_reports)
        header.addWidget(self.search_input)

        layout.addLayout(header)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "شماره گزارش", "نام بیمار / مشتری", "شناسه نمونه", "نوع نمونه", "وضعیت استخراج", "عملیات"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("background-color: #1a202c; border: 1px solid #2d3748;")
        layout.addWidget(self.table)

        self.load_reports()

    def load_reports(self):
        self.table.setRowCount(0)
        q_text = self.search_input.text().strip()

        with get_db_session() as s:
            query = s.query(LaboratoryReport)
            if q_text:
                query = query.filter(
                    LaboratoryReport.patient_name.like(f"%{q_text}%") |
                    LaboratoryReport.sample_id.like(f"%{q_text}%")
                )
            reps = query.order_by(LaboratoryReport.id.desc()).all()
            self.table.setRowCount(len(reps))

            for idx, r in enumerate(reps):
                self.table.setItem(idx, 0, QTableWidgetItem(r.report_number or ""))

                cust_name = "---"
                if r.customer:
                    cust_name = r.customer.display_name
                elif r.patient_name:
                    cust_name = r.patient_name

                self.table.setItem(idx, 1, QTableWidgetItem(cust_name))
                self.table.setItem(idx, 2, QTableWidgetItem(r.sample_id or ""))
                self.table.setItem(idx, 3, QTableWidgetItem(r.sample_type or ""))

                status_item = QTableWidgetItem(r.review_status or "جدید")
                self.table.setItem(idx, 4, status_item)

                view_btn = QPushButton("مشاهده")
                view_btn.setStyleSheet("background-color: #2d3748; color: white; max-width: 80px;")
                self.table.setCellWidget(idx, 5, view_btn)
