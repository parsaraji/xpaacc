import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True)
    invoice_number = Column(String, unique=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    report_id = Column(Integer, ForeignKey("laboratory_reports.id"), nullable=True)
    issue_date = Column(DateTime, default=datetime.datetime.utcnow)
    due_date = Column(DateTime, nullable=True)
    discount = Column(Numeric(18, 2), default=0.0)
    tax = Column(Numeric(18, 2), default=0.0)
    total_amount = Column(Numeric(18, 2), default=0.0)
    paid_amount = Column(Numeric(18, 2), default=0.0)
    payment_status = Column(String, default="تسویه‌نشده")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    customer = relationship("Customer", back_populates="invoices")
    report = relationship("LaboratoryReport", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice")
    transactions = relationship("FinancialTransaction", back_populates="invoice")

class InvoiceItem(Base):
    __tablename__ = "invoice_items"
    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    item_name = Column(String)
    quantity = Column(Integer, default=1)
    unit_price = Column(Numeric(18, 2), default=0.0)
    total_price = Column(Numeric(18, 2), default=0.0)

    invoice = relationship("Invoice", back_populates="items")
