from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.lab_test_catalog import LabTestCatalog

class CatalogRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, catalog_id: int) -> Optional[LabTestCatalog]:
        return self.session.query(LabTestCatalog).filter(LabTestCatalog.id == catalog_id).first()

    def get_by_code(self, test_code: str) -> Optional[LabTestCatalog]:
        return self.session.query(LabTestCatalog).filter(LabTestCatalog.test_code == test_code).first()

    def get_all(self) -> List[LabTestCatalog]:
        return self.session.query(LabTestCatalog).order_by(LabTestCatalog.test_code.asc()).all()

    def create(self, item: LabTestCatalog) -> LabTestCatalog:
        self.session.add(item)
        self.session.flush()
        return item
