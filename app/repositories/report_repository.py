from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.laboratory_report import LaboratoryReport, LaboratoryReportPage
from app.models.laboratory_test import LaboratoryTestResult

class ReportRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, report_id: int) -> Optional[LaboratoryReport]:
        return self.session.query(LaboratoryReport).filter(LaboratoryReport.id == report_id).first()

    def get_by_hash(self, file_hash: str) -> Optional[LaboratoryReport]:
        return self.session.query(LaboratoryReport).filter(LaboratoryReport.file_hash == file_hash).first()

    def get_all(self) -> List[LaboratoryReport]:
        return self.session.query(LaboratoryReport).order_by(LaboratoryReport.created_at.desc()).all()

    def get_by_customer_id(self, customer_id: int) -> List[LaboratoryReport]:
        return self.session.query(LaboratoryReport).filter(LaboratoryReport.customer_id == customer_id).all()

    def create(self, report: LaboratoryReport) -> LaboratoryReport:
        self.session.add(report)
        self.session.flush()
        return report

    def update(self, report: LaboratoryReport) -> LaboratoryReport:
        self.session.flush()
        return report
