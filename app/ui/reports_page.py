from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QLineEdit, QMessageBox, QDialog, QFormLayout, QDialogButtonBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from app.config import FONT_NAME
from app.database.session import get_db_session
from app.models.laboratory_report import LaboratoryReport
from app.models.laboratory_test import LaboratoryTestResult

class EditReportDialog(QDialog):
    def __init__(self, report_id: int, parent=None):
        super().__init__(parent)
        self.report_id = report_id
        self.setWindowTitle("ویرایش دستی گزارش آزمایشگاهی")
        self.setMinimumSize(850, 650) # Extremely large, spacious and highly readable popup
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Meta Form
        form = QFormLayout()
        self.patient_input = QLineEdit()
        self.sample_id_input = QLineEdit()

        form.addRow("نام بیمار:", self.patient_input)
        form.addRow("شناسه نمونه:", self.sample_id_input)
        layout.addLayout(form)

        # Tests Grid
        grid_lbl = QLabel("لیست تست‌ها:")
        grid_lbl.setFont(QFont(FONT_NAME, 10, QFont.Bold))
        layout.addWidget(grid_lbl)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["نام تست", "نتیجه", "واحد", "وضعیت"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        # Grid Control Buttons
        btn_layout = QHBoxLayout()
        add_row_btn = QPushButton("افزودن تست جدید")
        add_row_btn.clicked.connect(self.add_row)
        btn_layout.addWidget(add_row_btn)

        del_row_btn = QPushButton("حذف تست انتخابی")
        del_row_btn.clicked.connect(self.delete_row)
        btn_layout.addWidget(del_row_btn)
        layout.addLayout(btn_layout)

        # OK / Cancel Buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, parent=self)
        self.buttons.accepted.connect(self.save_data)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

        self.load_data()

    def load_data(self):
        with get_db_session() as s:
            rep = s.query(LaboratoryReport).filter(LaboratoryReport.id == self.report_id).first()
            if rep:
                self.patient_input.setText(rep.patient_name or "")
                self.sample_id_input.setText(rep.sample_id or "")

                tests = s.query(LaboratoryTestResult).filter(LaboratoryTestResult.report_id == self.report_id).all()
                self.table.setRowCount(len(tests))
                for idx, t in enumerate(tests):
                    self.table.setItem(idx, 0, QTableWidgetItem(t.test_name))
                    self.table.setItem(idx, 1, QTableWidgetItem(t.value_text or "---"))
                    self.table.setItem(idx, 2, QTableWidgetItem(t.unit or "---"))
                    self.table.setItem(idx, 3, QTableWidgetItem(t.result_status or "Normal"))

    def add_row(self):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem("T3"))
        self.table.setItem(row, 1, QTableWidgetItem("1.0"))
        self.table.setItem(row, 2, QTableWidgetItem("ng/mL"))
        self.table.setItem(row, 3, QTableWidgetItem("Normal"))

    def delete_row(self):
        selected_ranges = self.table.selectedRanges()
        if selected_ranges:
            row = selected_ranges[0].topRow()
            self.table.removeRow(row)

    def save_data(self):
        p_name = self.patient_input.text().strip()
        s_id = self.sample_id_input.text().strip()

        with get_db_session() as s:
            rep = s.query(LaboratoryReport).filter(LaboratoryReport.id == self.report_id).first()
            if rep:
                rep.patient_name = p_name
                rep.sample_id = s_id

                # Remove old tests
                s.query(LaboratoryTestResult).filter(LaboratoryTestResult.report_id == self.report_id).delete()

                # Add newly configured tests
                for r in range(self.table.rowCount()):
                    t_name = self.table.item(r, 0).text() if self.table.item(r, 0) else ""
                    val_text = self.table.item(r, 1).text() if self.table.item(r, 1) else ""
                    unit_text = self.table.item(r, 2).text() if self.table.item(r, 2) else ""
                    status_text = self.table.item(r, 3).text() if self.table.item(r, 3) else "Normal"

                    if t_name:
                        db_tr = LaboratoryTestResult(
                            report_id=self.report_id,
                            test_name=t_name,
                            value_text=val_text,
                            unit=unit_text,
                            result_status=status_text
                        )
                        s.add(db_tr)
                s.flush()

        self.accept()


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

        # Table Grid
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "شماره گزارش", "نام بیمار / مشتری", "شناسه نمونه", "نوع نمونه", "وضعیت استخراج", "عملیات کاربردی"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("background-color: #ffffff; border: 1px solid #e5e7eb;")
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

                cust_name = r.patient_name or "---"
                if r.customer:
                    cust_name = f"{r.customer.display_name} ({r.patient_name or ''})"

                self.table.setItem(idx, 1, QTableWidgetItem(cust_name))
                self.table.setItem(idx, 2, QTableWidgetItem(r.sample_id or ""))
                self.table.setItem(idx, 3, QTableWidgetItem(r.sample_type or ""))

                self.table.setItem(idx, 4, QTableWidgetItem(r.review_status or "جدید"))

                # User Action Operations layout
                widget = QWidget()
                w_layout = QHBoxLayout(widget)
                w_layout.setContentsMargins(4, 4, 4, 4)
                w_layout.setSpacing(4)

                confirm_btn = QPushButton("تأیید")
                confirm_btn.setStyleSheet("background-color: #10b981; color: white;")
                confirm_btn.clicked.connect(lambda checked=False, rid=r.id: self.confirm_report_status(rid))
                w_layout.addWidget(confirm_btn)

                edit_btn = QPushButton("ویرایش")
                edit_btn.setStyleSheet("background-color: #0284c7; color: white;")
                edit_btn.clicked.connect(lambda checked=False, rid=r.id: self.edit_report_details(rid))
                w_layout.addWidget(edit_btn)

                del_btn = QPushButton("حذف")
                del_btn.setStyleSheet("background-color: #ef4444; color: white;")
                del_btn.clicked.connect(lambda checked=False, rid=r.id: self.delete_report_record(rid))
                w_layout.addWidget(del_btn)

                self.table.setCellWidget(idx, 5, widget)

    def confirm_report_status(self, report_id: int):
        with get_db_session() as s:
            rep = s.query(LaboratoryReport).filter(LaboratoryReport.id == report_id).first()
            if rep:
                rep.review_status = "تأییدشده"
                s.flush()
                QMessageBox.information(self, "موفقیت", "وضعیت گزارش آزمایشگاهی با موفقیت به تأییدشده تغییر یافت.")
                self.load_reports()

    def edit_report_details(self, report_id: int):
        dialog = EditReportDialog(report_id, self)
        if dialog.exec() == QDialog.Accepted:
            QMessageBox.information(self, "موفقیت", "گزارش آزمایشگاهی به صورت دستی اصلاح گردید.")
            self.load_reports()

    def delete_report_record(self, report_id: int):
        reply = QMessageBox.question(self, "تأیید حذف", "آیا از حذف این گزارش مطمئن هستید؟", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            with get_db_session() as s:
                s.query(LaboratoryTestResult).filter(LaboratoryTestResult.report_id == report_id).delete()
                s.query(LaboratoryReport).filter(LaboratoryReport.id == report_id).delete()
                s.flush()
                QMessageBox.information(self, "موفقیت", "گزارش آزمایشگاهی انتخابی با موفقیت حذف گردید.")
                self.load_reports()
