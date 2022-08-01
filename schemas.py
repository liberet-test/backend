from pydantic import BaseModel
from fastapi import Body
from typing import Optional

class Recharge(BaseModel):
    amount: int = Body(title="Amount to recharge")
    
    class Config:
        schema_extra = {
            "example": {
                "amount": 100
            }
        }

class TransactionORM(BaseModel):
    id: int
    supplier_id: int
    service_id: int
    income: bool
    quantity: int
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
    name: str = Body(description="Service name")
    price: int = Body(description="Service price")
    icon_url: str | None
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "string",
                "price": 100,
                "icon_url": "string or None"
            }
        }