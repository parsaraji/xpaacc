from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database.connection import Base
import datetime

class Attachment(Base):
    __tablename__ = "attachments"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    report_id = Column(Integer, ForeignKey("laboratory_reports.id"), nullable=True)
    filename = Column(String)
    file_path = Column(String)
    file_type = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
