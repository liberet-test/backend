from typing import List
from fastapi import APIRouter, Response, status
from database import Database
from entities import Service
import schemas

router = APIRouter()
database = Database()
# database.drop()
# database = Database()
# database.init()
session = database.get_session()

@router.get(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=List[schemas.ServiceORM]
    )
def get_services():
    """Obtiene todos los servicios"""
    services = session.query(Service).all()

    return services

@router.get(
    "/{service_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ServiceORM
    )
def get_service_by_id(service_id: int):
    """Obtiene un servicio por su id"""
    service = session.query(Service).filter(Service.id == service_id).one()
    
    print(service)

    return service

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=bool
    )
def create_service(service: schemas.ServiceORM):
    """Crea un nuevo servicio"""
    service = Service(
        name = service.name,
        price = service.price,
        icon_url = service.icon_url
    )
    session.add(service)
    session.commit()

    return True