from sqlalchemy import Column, Integer, String, Numeric, DateTime
from app.database.connection import Base
import datetime

class LabTestCatalog(Base):
    __tablename__ = "lab_test_catalog"

    id = Column(Integer, primary_key=True, index=True)
    test_code = Column(String, unique=True, index=True, nullable=False) # e.g., T3, T4, TSH, SGPT
    full_name = Column(String, nullable=True) # e.g., Thyroid Stimulating Hormone
    default_unit = Column(String, nullable=True) # e.g., uIU/mL
    reference_range = Column(String, nullable=True) # e.g., 0.4 - 4.0
    default_fee = Column(Numeric(precision=18, scale=2), default=0.0) # pricing/price tag
    category = Column(String, default="General") # e.g., Thyroid, Liver, Hematology
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
