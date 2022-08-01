import json
from typing import List
from fastapi import Body, FastAPI, HTTPException, status
from pydantic import BaseModel, Field, ValidationError
import uvicorn
from database import Database
from entities import Supplier, Transaction


app = FastAPI(
    swagger_ui_parameters={"deepLinking": False},
    docs_url="/api/v1/docs",
    title="Wallet API",
    description="Liberet Challenge",
    version="2.0",
    openapi_url="/api/v1/openapi.json"
    )

# Starting new database
database = Database()
# database.init()
session = database.get_session()

class Recharge(BaseModel):
    amount: int = Body(description="Amount to recharge")
    
    class Config:
        schema_extra = {
            "example": {
                "amount": 100
            }
        }

class TransactionORM(BaseModel):
    id: int = Body(description="Transaction ID")
    supplier_id: int = Body(description="Supplier id")
    service_id: int = Body(description="Service id")
    income: bool = Body(description="Income")
    quantity: int = Body(description="Quantity")
    credits: int = Body(description="Credits")
    
    class Config:
        orm_mode = True

@app.patch("/supplier/{supplier_id}/wallet/recharge", tags=["Wallet"], status_code=status.HTTP_200_OK, response_model=bool)
async def make_recharge(recharge: Recharge, supplier_id: int):
    """Añande créditos a la billetera del proveedor"""
    if recharge.amount < 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")

    supplier = session.query(Supplier).filter(Supplier.id == supplier_id).one()
    
    supplier.credits += recharge.amount
    
    transaction = Transaction(
        supplier_id = supplier_id,
        service_id = 3,
        income = True,
        credits = recharge.amount
    )
    
    session.add(transaction)
    session.commit()

    return True

@app.get("/supplier/{supplier_id}/wallet/transaction", tags=["Wallet"], status_code=status.HTTP_200_OK, response_model=List[TransactionORM])
async def get_transactions(supplier_id: int):
    """Obtiene todas las transacciones del proveedor"""
    transactions = session.query(Transaction).all()

    return transactions







# Drop database when application is closed
# @app.on_event('shutdown')
# def shutdown_event():
#     database.drop()
#     print("Database dropped")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)