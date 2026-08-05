from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Numeric
from sqlalchemy.orm import relationship
from app.database.connection import Base
import datetime

class ExtractionTemplate(Base):
    __tablename__ = "extraction_templates"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    laboratory_name = Column(String, nullable=True)
    width = Column(Numeric(10, 2), nullable=True)
    height = Column(Numeric(10, 2), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    reports = relationship("LaboratoryReport", back_populates="template")
    fields = relationship("ExtractionField", back_populates="template", cascade="all, delete-orphan")

class ExtractionField(Base):
    __tablename__ = "extraction_fields"
    id = Column(Integer, primary_key=True)
    template_id = Column(Integer, ForeignKey("extraction_templates.id"))
    field_name = Column(String) # e.g. Patient, Test, etc.
    x0 = Column(Numeric(10, 2))
    y0 = Column(Numeric(10, 2))
    x1 = Column(Numeric(10, 2))
    y1 = Column(Numeric(10, 2))
    rule_type = Column(String) # LABEL_VALUE, REGEX, TABLE_COLUMN

    template = relationship("ExtractionTemplate", back_populates="fields")
