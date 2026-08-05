from sqlalchemy.orm import Session
from app.models.laboratory_report import LaboratoryReport
from app.repositories.report_repository import ReportRepository
import hashlib

class ReportService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = ReportRepository(session)

    def calculate_file_hash(self, file_content: bytes) -> str:
        return hashlib.sha256(file_content).hexdigest()

    def register_report(self, report_data: dict, file_content: bytes = None) -> LaboratoryReport:
        file_hash = None
        if file_content:
            file_hash = self.calculate_file_hash(file_content)
            existing = self.repo.get_by_hash(file_hash)
            if existing:
                raise ValueError("این فایل قبلاً وارد شده است و تکراری می‌باشد.")

        rep = LaboratoryReport(
            report_number=report_data.get("report_number"),
            customer_id=report_data.get("customer_id"),
            patient_name=report_data.get("patient_name"),
            sample_id=report_data.get("sample_id"),
            sample_type=report_data.get("sample_type"),
            test_date=report_data.get("test_date"),
            send_date=report_data.get("send_date"),
            print_date=report_data.get("print_date"),
            file_hash=file_hash,
            original_filename=report_data.get("original_filename"),
            review_status="جدید"
        )
        self.repo.create(rep)
        self.session.flush()
        return rep
