import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.database.connection import Base

class FinancialTransaction(Base):
    __tablename__ = "financial_transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_number = Column(String, unique=True, index=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    transaction_type = Column(String, nullable=False)  # Opening balance, Sales invoice, Debit transaction, Credit transaction, Payment received, Payment made, Discount, Refund, Adjustment, Cancellation, Reversal
    transaction_date = Column(DateTime, default=datetime.datetime.utcnow)
    due_date = Column(DateTime, nullable=True)
    description = Column(String, nullable=True)
    reference_number = Column(String, nullable=True)
    debit_amount = Column(Numeric(precision=18, scale=2), default=0.0)
    credit_amount = Column(Numeric(precision=18, scale=2), default=0.0)
    running_balance = Column(Numeric(precision=18, scale=2), default=0.0)
    currency = Column(String, default="Toman")  # Toman or Rial
    payment_method = Column(String, nullable=True) # نقدی, کارت‌خوان, کارت به کارت, چک, etc.
    status = Column(String, default="ثبت‌شده") # پیش‌نویس، ثبت‌شده، بخشی تسویه‌شده، تسویه‌شده، لغوشده

    report_id = Column(Integer, ForeignKey("laboratory_reports.id"), nullable=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=True)
    reversal_transaction_id = Column(Integer, ForeignKey("financial_transactions.id"), nullable=True)

    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    customer = relationship("Customer", back_populates="transactions")
    report = relationship("LaboratoryReport", back_populates="transactions")
    invoice = relationship("Invoice", back_populates="transactions")
