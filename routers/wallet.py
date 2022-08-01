from typing import List
from fastapi import APIRouter, status, Response
from entities import Supplier, Transaction, Service
import schemas

router = APIRouter()

@router.patch(
    "/supplier/{supplier_id}/wallet/recharge",
    tags=["Wallet"],
    status_code=status.HTTP_200_OK,
    response_model=bool|dict
    )
async def make_recharge(recharge: schemas.Recharge, supplier_id: int, response: Response):
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

@router.get(
    "/supplier/{supplier_id}/wallet/transaction",
    tags=["Wallet"],
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.TransactionORM]
    )
async def get_transactions(supplier_id: int):
    """Obtiene todas las transacciones del proveedor"""
    transactions = session.query(Transaction).filter(Transaction.supplier_id == supplier_id).all()

    return transactions


@router.post(
    "/supplier/{supplier_id}/wallet/service/{service_id}",
    tags=["Wallet"],
    status_code=status.HTTP_200_OK,
    response_model=bool
    )
async def use_service(supplier_id: int, service_id: int, response: Response):
    """Usa un servicio de los disponibles"""

    # Validando que tenga los créditos suficientes
    supplier = session.query(Supplier).filter(Supplier.id == supplier_id).one()
    service = session.query(Service).filter(Service.id == service_id).one()
    if supplier.credits < service.price:
        response.status_code = 424
        return {"message": "Not enough credits"}

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

@router.post(
    "/supplier/{supplier_id}/wallet/service/{service_id}/{quantity}",
    tags=["Wallet"],
    status_code=status.HTTP_200_OK,
    response_model=bool|dict
    )
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