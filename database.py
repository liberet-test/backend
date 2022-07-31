import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from entities import Base, Service, Supplier

load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database = os.getenv("DB_DATABASE")

# Connect to the database
if os.getenv("ENVIRONMENT") == 'development':
    engine = create_engine(
        f"mysql://{user}:{password}@{host}", echo=True)
else:
    engine = create_engine(
        f"mysql://{user}:{password}@{host}")

# Create database
def create():
    engine.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
    engine.execute(f"USE {database}")

    Base.metadata.create_all(engine)

    with Session(engine) as session:

        service1 = Service(
            name="nuevo producto",
            price="5",
            icon_url='/home/ivan/Projects/personal/liberet-test/database/icons/1.png'
        )
        service2 = Service(
            name="lanzar campaña de marketing",
            price="1",
            icon_url='/home/ivan/Projects/personal/liberet-test/database/icons/megafono.png'
        )

        liberet = Supplier(name="Liberet", credits=100)

        session.add_all([service1, service2, liberet])

        session.commit()

def drop():
    engine.execute(f"DROP DATABASE IF EXISTS {database}")
    Base.metadata.drop_all(engine)
