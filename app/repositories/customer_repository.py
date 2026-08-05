from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.customer import Customer
from app.models.customer_meta import CustomerAddress, CustomerTag

class CustomerRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        return self.session.query(Customer).filter(Customer.id == customer_id).first()

    def get_by_code(self, customer_code: str) -> Optional[Customer]:
        return self.session.query(Customer).filter(Customer.customer_code == customer_code).first()

    def get_by_mobile(self, mobile: str) -> Optional[Customer]:
        return self.session.query(Customer).filter(Customer.mobile == mobile).first()

    def get_all(self, include_archived: bool = False) -> List[Customer]:
        query = self.session.query(Customer)
        if not include_archived:
            query = query.filter(Customer.is_archived == False)
        return query.order_by(Customer.created_at.desc()).all()

    def create(self, customer: Customer) -> Customer:
        self.session.add(customer)
        self.session.flush()
        return customer

    def update(self, customer: Customer) -> Customer:
        self.session.flush()
        return customer

    def get_next_customer_code(self) -> str:
        last_cust = self.session.query(Customer).order_by(Customer.id.desc()).first()
        if last_cust:
            try:
                num = int(last_cust.customer_code.split("-")[1])
                return f"CUS-{(num + 1):06d}"
            except Exception:
                pass
        return "CUS-000001"
