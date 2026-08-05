import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    customer_code = Column(String, unique=True, index=True, nullable=False)
    customer_type = Column(String, nullable=False)  # شخص حقیقی, شخص حقوقی, دامپزشک, etc.
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    display_name = Column(String, nullable=False)
    company_name = Column(String, nullable=True)
    mobile = Column(String, index=True, nullable=False)
    secondary_mobile = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    national_id = Column(String, unique=True, nullable=True)
    economic_code = Column(String, nullable=True)
    registration_number = Column(String, nullable=True)
    province = Column(String, nullable=True)
    city = Column(String, nullable=True)
    address = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    credit_limit = Column(Numeric(precision=18, scale=2), default=0.0)
    opening_balance = Column(Numeric(precision=18, scale=2), default=0.0)
    opening_balance_type = Column(String, default="DEBIT")  # DEBIT, CREDIT, NONE
    current_balance = Column(Numeric(precision=18, scale=2), default=0.0)
    notes = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_archived = Column(Boolean, default=False)
    profile_image_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    addresses = relationship("CustomerAddress", back_populates="customer", cascade="all, delete-orphan")
    tags = relationship("CustomerTag", back_populates="customer", cascade="all, delete-orphan")
    reports = relationship("LaboratoryReport", back_populates="customer")
    transactions = relationship("FinancialTransaction", back_populates="customer")
    invoices = relationship("Invoice", back_populates="customer")
