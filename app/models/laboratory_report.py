import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from app.database.connection import Base

class LaboratoryReport(Base):
    __tablename__ = "laboratory_reports"

    id = Column(Integer, primary_key=True, index=True)
    report_number = Column(String, unique=True, index=True, nullable=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    patient_name = Column(String, nullable=True)
    patient_code = Column(String, nullable=True)
    customer_code = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    age = Column(String, nullable=True)
    blood_type = Column(String, nullable=True)
    species = Column(String, nullable=True)
    breed = Column(String, nullable=True)
    owner_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    sample_id = Column(String, index=True, nullable=True)
    sample_type = Column(String, nullable=True)
    mrn = Column(String, nullable=True)
    zone = Column(String, nullable=True)
    bed_number = Column(String, nullable=True)
    sender = Column(String, nullable=True)
    sent_from = Column(String, nullable=True)
    priority = Column(String, nullable=True)
    characteristic = Column(String, nullable=True)
    diagnosis = Column(Text, nullable=True)

    laboratory_name = Column(String, nullable=True)
    test_date = Column(String, nullable=True)
    send_date = Column(String, nullable=True)
    print_date = Column(String, nullable=True)
    registration_date = Column(String, nullable=True)
    tester = Column(String, nullable=True)
    reviewed_by = Column(String, nullable=True)
    notes = Column(Text, nullable=True)

    original_filename = Column(String, nullable=True)
    stored_file_path = Column(String, nullable=True)
    file_hash = Column(String, unique=True, index=True, nullable=True)
    page_count = Column(Integer, default=1)
    extraction_method = Column(String, default="NATIVE") # NATIVE, OCR, MANUAL
    extraction_confidence = Column(Numeric(precision=5, scale=2), default=100.0)

    raw_text = Column(Text, nullable=True)
    cleaned_text = Column(Text, nullable=True)
    template_id = Column(Integer, ForeignKey("extraction_templates.id"), nullable=True)
    review_status = Column(String, default="جدید") # جدید، در حال بررسی، تأییدشده، بایگانی‌شده، ناموفق
    financial_status = Column(String, default="بررسی نشده")

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    customer = relationship("Customer", back_populates="reports")
    template = relationship("ExtractionTemplate", back_populates="reports")
    pages = relationship("LaboratoryReportPage", back_populates="report", cascade="all, delete-orphan")
    results = relationship("LaboratoryTestResult", back_populates="report", cascade="all, delete-orphan")
    transactions = relationship("FinancialTransaction", back_populates="report")
    invoices = relationship("Invoice", back_populates="report")

class LaboratoryReportPage(Base):
    __tablename__ = "laboratory_report_pages"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("laboratory_reports.id"), nullable=False)
    page_number = Column(Integer, nullable=False)
    image_path = Column(String, nullable=True)
    raw_text = Column(Text, nullable=True)
    cleaned_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    report = relationship("LaboratoryReport", back_populates="pages")
