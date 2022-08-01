from typing import List, Optional
from fastapi import APIRouter, status, Response
from sqlalchemy import func
from database import Database
from entities import Supplier, Transaction, Service
import schemas

router = APIRouter()
database = Database()
session = database.get_session()

@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.TransactionORM]
)
async def get_transactions(supplier_id: int):
    """Obtiene todas las transacciones del proveedor"""
    transactions = session.query(Transaction).filter(Transaction.supplier_id == supplier_id).all()

    return transactions

@router.patch(
    "/recharge",
    status_code=status.HTTP_200_OK,
    response_model=dict
)
async def recharge_wallet(recharge: schemas.Recharge, supplier_id: int):
    """Añade créditos a la billetera del proveedor"""

    supplier = session.query(Supplier).filter(Supplier.id == supplier_id).one()
    
    supplier.credits += recharge.amount
    
    transaction = Transaction(
        supplier_id = supplier_id,
        service_id = 3,
        credits = recharge.amount
    )
    
    session.add(transaction)
    session.commit()

    return {"message": "Recharge successful"}

@router.post(
    "",
    status_code=status.HTTP_200_OK,
    response_model=dict
)
async def do_transaction(response: Response, supplier_id: int, service: schemas.UseService):
    """Genera una transaccion usando un servicio"""
    service_id = service.service_id
    quantity = service.quantity
    
    supplier = session.query(Supplier).filter(Supplier.id == supplier_id).one()
    service = session.query(Service).filter(Service.id == service_id).one()

    service_price = service.price * quantity
    
    if supplier.credits < service_price:
        response.status_code = 424
        return {"message": "Not enough credits"}

    # Generando la transacción
    transaction = Transaction(
        supplier_id = supplier_id,
        service_id = service_id,
        credits = service_price
    )
    session.add(transaction)
    
    # Descuentando créditos
    supplier.credits -= service_price
    
    session.commit()
    
    return {"message": "Transaction successful"}

@router.get(
    "/analytics",
    status_code=status.HTTP_200_OK,
    response_model=dict
)
async def get_credits_by_service(supplier_id: int):
    """Regresa el total de créditos usados por cada servicio"""
    results = session.query(Service.name, func.sum(Transaction.credits).label("credits"))\
    .join(Transaction)\
    .filter(Service.income == False)\
    .group_by(Service.id).all()
    
    return results