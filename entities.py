from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Supplier(Base):
    __tablename__ = 'suppliers'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    image_url = Column(String(255), default="https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y&s=128")
    credits = Column(Integer, default=0)
    transactions = relationship("Transaction", back_populates="supplier", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Supplier(id={self.id!r}, name={self.name!r})"

class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    icon_url = Column(String(255), nullable=False)
    transactions = relationship("Transaction", back_populates="service", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Service(id={self.id!r}, name={self.name!r}, price={self.price!r})"

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_cost = Column(Integer, nullable=False)
    
    supplier = relationship("Supplier", back_populates="transactions")
    service = relationship("Service", back_populates="transactions")

    def __repr__(self) -> str:
        return f"Transaction(id={self.id!r}, supplier_id={self.supplier_id!r}, service_id={self.service_id!r}, quantity={self.quantity!r}, total={self.total!r})"