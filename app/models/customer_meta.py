import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base

class CustomerAddress(Base):
    __tablename__ = "customer_addresses"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    title = Column(String, nullable=False)  # محل کار، منزل، دفتر مرکزی
    province = Column(String, nullable=True)
    city = Column(String, nullable=True)
    address_line = Column(String, nullable=False)
    postal_code = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    customer = relationship("Customer", back_populates="addresses")

class CustomerTag(Base):
    __tablename__ = "customer_tags"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    tag_name = Column(String, nullable=False)

    customer = relationship("Customer", back_populates="tags")
