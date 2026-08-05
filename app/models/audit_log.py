from sqlalchemy import Column, Integer, String, DateTime, Text
from app.database.connection import Base
import datetime

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    action_type = Column(String) # e.g. Customer Creation, Report Editing, etc.
    entity_type = Column(String)
    entity_id = Column(Integer, nullable=True)
    previous_values = Column(Text, nullable=True)
    new_values = Column(Text, nullable=True)
    user = Column(String, default="Admin")
    device_info = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
