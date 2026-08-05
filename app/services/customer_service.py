import datetime
from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository
from app.services.accounting_service import AccountingService
from decimal import Decimal

class CustomerService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = CustomerRepository(session)
        self.accounting = AccountingService(session)

    def create_customer(self, customer_data: dict) -> Customer:
        code = self.repo.get_next_customer_code()

        mobile = customer_data.get("mobile")
        if mobile and self.repo.get_by_mobile(mobile):
            raise ValueError("مشتری با این شماره همراه قبلاً ثبت شده است.")

        cust = Customer(
            customer_code=code,
            customer_type=customer_data.get("customer_type", "شخص حقیقی"),
            first_name=customer_data.get("first_name"),
            last_name=customer_data.get("last_name"),
            display_name=customer_data.get("display_name"),
            company_name=customer_data.get("company_name"),
            mobile=mobile,
            secondary_mobile=customer_data.get("secondary_mobile"),
            phone=customer_data.get("phone"),
            email=customer_data.get("email"),
            national_id=customer_data.get("national_id"),
            economic_code=customer_data.get("economic_code"),
            registration_number=customer_data.get("registration_number"),
            province=customer_data.get("province"),
            city=customer_data.get("city"),
            address=customer_data.get("address"),
            postal_code=customer_data.get("postal_code"),
            credit_limit=customer_data.get("credit_limit", Decimal("0.00")),
            opening_balance=customer_data.get("opening_balance", Decimal("0.00")),
            opening_balance_type=customer_data.get("opening_balance_type", "NONE"),
            is_active=customer_data.get("is_active", True)
        )
        self.repo.create(cust)
        self.session.flush()

        if cust.opening_balance > 0:
            debit = Decimal("0.00")
            credit = Decimal("0.00")
            if cust.opening_balance_type == "DEBIT":
                debit = cust.opening_balance
            elif cust.opening_balance_type == "CREDIT":
                credit = cust.opening_balance

            self.accounting.post_transaction(
                customer_id=cust.id,
                transaction_type="Opening balance",
                debit_amount=debit,
                credit_amount=credit,
                description="ثبت مانده حساب افتتاحیه"
            )
        return cust

    def update_customer(self, customer_id: int, updated_data: dict) -> Customer:
        cust = self.repo.get_by_id(customer_id)
        if not cust:
            raise ValueError("مشتری یافت نشد.")

        for k, v in updated_data.items():
            if hasattr(cust, k):
                setattr(cust, k, v)
        self.repo.update(cust)
        self.session.flush()
        return cust
