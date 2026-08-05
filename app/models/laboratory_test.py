import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.database.connection import Base

class LaboratoryTestResult(Base):
    __tablename__ = "laboratory_test_results"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("laboratory_reports.id"), nullable=False)
    row_number = Column(Integer, nullable=True)
    test_name = Column(String, index=True, nullable=False) # e.g., SGPT
    full_name = Column(String, nullable=True)
    value_text = Column(String, nullable=True) # e.g., 16.1, >100, Positive
    numeric_value = Column(Numeric(precision=18, scale=4), nullable=True)
    unit = Column(String, nullable=True) # e.g., U/L
    result_status = Column(String, nullable=True) # e.g., Normal, High
    remark = Column(String, nullable=True)
    reference_text = Column(String, nullable=True)
    reference_min = Column(Numeric(precision=18, scale=4), nullable=True)
    reference_max = Column(Numeric(precision=18, scale=4), nullable=True)
    abnormal_flag = Column(String, nullable=True) # H, L, *, Normal
    confidence = Column(Numeric(precision=5, scale=2), default=100.0)
    source_page = Column(Integer, default=0)
    source_bbox = Column(String, nullable=True) # JSON or simple bounding box coordinates string "x0,y0,x1,y1"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    report = relationship("LaboratoryReport", back_populates="results")
