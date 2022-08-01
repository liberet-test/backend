import json
from typing import List, Optional
from urllib import response
from fastapi import Body, FastAPI, HTTPException, status, Response
from pydantic import BaseModel
import uvicorn
from database import Database
from entities import Supplier, Transaction, Service

# TODO: Refactorizaaaaar
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

class SupplierORM(BaseModel):
    id: int = Body(description="Supplier ID")
    name: str = Body(description="Supplier name")
    image_url: str = Body(description="Supplier image url")
    credits: int = Body(description="Supplier credits")
    
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

@app.patch("/supplier/{supplier_id}/wallet/recharge", tags=["Wallet"], status_code=status.HTTP_200_OK, response_model=bool|dict)
async def make_recharge(recharge: Recharge, supplier_id: int, response: Response):
    """Añade créditos a la billetera del proveedor"""
    if recharge.amount < 0:
        response.status_code = 424
        return {"message": "Amount must be greater than 0"}

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
    transactions = session.query(Transaction).filter(Transaction.supplier_id == supplier_id).all()

    return transactions


@app.post("/supplier/{supplier_id}/wallet/service/{service_id}", tags=["Wallet"], status_code=status.HTTP_200_OK, response_model=bool)
async def use_service(supplier_id: int, service_id: int):
    """Usa un servicio de los disponibles"""

    # Validando que tenga los créditos suficientes
    supplier = session.query(Supplier).filter(Supplier.id == supplier_id).one()
    service = session.query(Service).filter(Service.id == service_id).one()
    if supplier.credits < service.price:
        raise HTTPException(status_code=424, detail="Not enough credits")

    # Generando la transacción
    transaction = Transaction(
        supplier_id = supplier_id,
        service_id = service_id,
        credits = service.price
    )
    
    # Descuentando créditos
    supplier.credits -= service.price
    
    session.add(transaction)
    session.commit()
    
    return True

@app.post("/supplier/{supplier_id}/wallet/service/{service_id}/{quantity}", tags=["Wallet"], status_code=status.HTTP_200_OK, response_model=bool|dict)
async def use_service_in_quantity(supplier_id: int, service_id: int, quantity: int, response: Response):
    """Usa un servicio de los disponibles"""

    # Validando que tenga los créditos suficientes
    supplier = session.query(Supplier).filter(Supplier.id == supplier_id).one()
    service = session.query(Service).filter(Service.id == service_id).one()
    total_cost = service.price * quantity
    if supplier.credits < total_cost:
        response.status_code = 424
        return {"message": "Not enough credits"}

    # Generando la transacción
    transaction = Transaction(
        supplier_id = supplier_id,
        service_id = service_id,
        credits = service.price
    )
    
    # Descuentando créditos
    supplier.credits -= total_cost
    
    session.add(transaction)
    session.commit()
    
    return True

@app.get("/service", tags=["Service"], status_code=status.HTTP_201_CREATED, response_model=List[ServiceORM])
def get_services():
    """Obtiene todos los servicios"""
    services = session.query(Service).all()

    return services

@app.get("/service/{service_id}", tags=["Service"], status_code=status.HTTP_201_CREATED, response_model=ServiceORM)
def get_service_by_id(service_id: int):
    """Obtiene todos los servicios"""
    service = session.query(Service).filter(Service.id == service_id).one()

    return service

@app.post("/service", tags=["Service"], status_code=status.HTTP_201_CREATED, response_model=bool)
def create_service(service: ServiceORM):
    """Crea un nuevo servicio"""
    service = Service(
        name = service.name,
        price = service.price,
        icon_url = service.icon_url
    )
    session.add(service)
    session.commit()

    return True

@app.delete("/service", tags=["Service"], status_code=status.HTTP_201_CREATED, response_model=bool)
def delete_service(service_id: int):
    """Borra un servicio"""
    session.query(Service).filter(Service.id == service_id).delete()
    session.commit()

    return True

# Drop database when application is closed
# @app.on_event('shutdown')
# def shutdown_event():
#     database.drop()
#     print("Database dropped")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)