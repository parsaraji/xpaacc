from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.transaction import FinancialTransaction

class TransactionRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, transaction_id: int) -> Optional[FinancialTransaction]:
        return self.session.query(FinancialTransaction).filter(FinancialTransaction.id == transaction_id).first()

    def get_by_number(self, transaction_number: str) -> Optional[FinancialTransaction]:
        return self.session.query(FinancialTransaction).filter(FinancialTransaction.transaction_number == transaction_number).first()

    def get_by_customer_id(self, customer_id: int) -> List[FinancialTransaction]:
        return self.session.query(FinancialTransaction).filter(FinancialTransaction.customer_id == customer_id).order_by(FinancialTransaction.transaction_date.asc()).all()

    def create(self, transaction: FinancialTransaction) -> FinancialTransaction:
        self.session.add(transaction)
        self.session.flush()
        return transaction

    def get_next_transaction_number(self) -> str:
        last_tx = self.session.query(FinancialTransaction).order_by(FinancialTransaction.id.desc()).first()
        if last_tx:
            try:
                num = int(last_tx.transaction_number.split("-")[1])
                return f"TXN-{(num + 1):06d}"
            except Exception:
                pass
        return "TXN-100001"
