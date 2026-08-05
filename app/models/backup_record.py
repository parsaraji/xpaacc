from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.database.connection import Base
import datetime

class BackupRecord(Base):
    __tablename__ = "backup_records"
    id = Column(Integer, primary_key=True)
    backup_path = Column(String)
    file_size_kb = Column(Integer)
    is_auto = Column(Boolean, default=False)
    status = Column(String, default="موفق")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
