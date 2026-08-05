from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.invoice import Invoice

class InvoiceRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, invoice_id: int) -> Optional[Invoice]:
        return self.session.query(Invoice).filter(Invoice.id == invoice_id).first()

    def get_by_number(self, invoice_number: str) -> Optional[Invoice]:
        return self.session.query(Invoice).filter(Invoice.invoice_number == invoice_number).first()

    def get_by_customer_id(self, customer_id: int) -> List[Invoice]:
        return self.session.query(Invoice).filter(Invoice.customer_id == customer_id).all()

    def create(self, invoice: Invoice) -> Invoice:
        self.session.add(invoice)
        self.session.flush()
        return invoice

    def get_next_invoice_number(self) -> str:
        last_inv = self.session.query(Invoice).order_by(Invoice.id.desc()).first()
        if last_inv:
            try:
                parts = last_inv.invoice_number.split("-")
                num = int(parts[2])
                return f"INV-2026-{(num + 1):04d}"
            except Exception:
                pass
        return "INV-2026-0001"
