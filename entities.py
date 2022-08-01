from email.policy import default
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Supplier(Base):
    __tablename__ = 'suppliers'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    image_url = Column(String(255), default="https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y&s=128")
    credits = Column(Integer, default=0)
    transactions = relationship("Transaction", back_populates="supplier", cascade="all, delete-orphan")


class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    icon_url = Column(String(255), nullable=False)
    transactions = relationship("Transaction", back_populates="service", cascade="all, delete-orphan")


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    income = Column(Boolean, nullable=False, default=False)
    quantity = Column(Integer, nullable=False, default=1)
    credits = Column(Integer, nullable=False)
    
    supplier = relationship("Supplier", back_populates="transactions")
    service = relationship("Service", back_populates="transactions")
