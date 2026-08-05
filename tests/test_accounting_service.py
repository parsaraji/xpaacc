import pytest
from decimal import Decimal
from app.database.connection import Base, create_engine
from sqlalchemy.orm import sessionmaker
from app.services.accounting_service import AccountingService
from app.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_ledger_debit_credit_calculation(db_session):
    cust_repo = CustomerRepository(db_session)
    accounting = AccountingService(db_session)

    # 1. Create a customer
    cust = Customer(
        customer_code="CUS-9999",
        customer_type="شخص حقیقی",
        display_name="تست لجر",
        mobile="09000000000",
        opening_balance=Decimal("100.00"),
        opening_balance_type="DEBIT",
        current_balance=Decimal("100.00")
    )
    cust_repo.create(cust)
    db_session.commit()

    # Create the opening transaction
    accounting.post_transaction(
        customer_id=cust.id,
        transaction_type="Opening balance",
        debit_amount=Decimal("100.00"),
        credit_amount=Decimal("0.00"),
        description="مانده اولیه"
    )

    # 2. Add a debit charge (e.g. Sales Invoice)
    accounting.post_transaction(
        customer_id=cust.id,
        transaction_type="Sales invoice",
        debit_amount=Decimal("250.00"),
        credit_amount=Decimal("0.00"),
        description="فاکتور تست"
    )

    # Balance should be 350.00
    db_session.refresh(cust)
    assert cust.current_balance == Decimal("350.00")

    # 3. Add a payment received (credit)
    accounting.post_transaction(
        customer_id=cust.id,
        transaction_type="Customer payment received",
        debit_amount=Decimal("0.00"),
        credit_amount=Decimal("150.00"),
        description="دریافتی تست"
    )

    # Balance should be 200.00
    db_session.refresh(cust)
    assert cust.current_balance == Decimal("200.00")
