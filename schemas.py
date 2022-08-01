from pydantic import BaseModel
from fastapi import Body
from typing import Optional

class Recharge(BaseModel):
    amount: int
    
    class Config:
        schema_extra = {
            "example": {
                "amount": 100
            }
        }

class UseService(BaseModel):
    service_id: int
    quantity: int
    
    class Config:
        schema_extra = {
            "example": {
                "service_id": 1,
                "quantity": 5
            }
        }

class TransactionORM(BaseModel):
    id: int
    supplier_id: int
    service_id: int
    credits: int
    
    class Config:
        orm_mode = True

class SupplierORM(BaseModel):
    id: int
    name: str
    image_url: str
    credits: int
    
    class Config:
        orm_mode = True

class ServiceORM(BaseModel):
    id: int = Optional[None]
    name: str
    income: bool = Optional[None]
    price: int
    icon_url: str = "/home/ivan/Projects/personal/liberet-test/backend/icons/1.png"
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "string",
                "price": 100,
                "income": False,
                "icon_url": "string or None"
            }
        }