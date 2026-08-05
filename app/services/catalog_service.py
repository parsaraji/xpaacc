from sqlalchemy.orm import Session
from app.repositories.catalog_repository import CatalogRepository
from app.models.lab_test_catalog import LabTestCatalog
from decimal import Decimal

class CatalogService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = CatalogRepository(session)

    def register_test_item(self, code: str, full_name: str, unit: str, ref_range: str, fee: Decimal, category: str = "General") -> LabTestCatalog:
        existing = self.repo.get_by_code(code)
        if existing:
            raise ValueError(f"یک تست آزمایشگاهی با کد {code} از قبل در کاتالوگ وجود دارد.")

        item = LabTestCatalog(
            test_code=code,
            full_name=full_name,
            default_unit=unit,
            reference_range=ref_range,
            default_fee=fee,
            category=category
        )
        self.repo.create(item)
        self.session.flush()
        return item
