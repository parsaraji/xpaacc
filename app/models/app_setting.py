from sqlalchemy import Column, Integer, String, Text
from app.database.connection import Base

class AppSetting(Base):
    __tablename__ = "app_settings"
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True)
    value = Column(Text)
