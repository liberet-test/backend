import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from entities import Base, Service, Supplier

load_dotenv()

class Database:
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    name = os.getenv("DB_DATABASE")
    
    def __init__(self) -> None:
        # Connect client
        self.engine = create_engine(f"mysql://{self.user}:{self.password}@{self.host}")

        # Create database
        self.engine.execute(f"CREATE DATABASE IF NOT EXISTS {self.name}")
        self.engine.execute(f"USE {self.name}")


    def get_session(self) -> Session:
        return Session(self.engine)

    def init(self) -> Session:
        """Create default data

        Returns:
            Session: Connection to database
        """

        Base.metadata.create_all(self.engine)
        with Session(self.engine) as session:
            # Create default data
            service1 = Service(
                name="nuevo producto",
                price="5",
                icon_url='/home/ivan/Projects/personal/liberet-test/backend/icons/1.png'
            )
            service2 = Service(
                name="lanzar campaña de marketing",
                price="1",
                icon_url='/home/ivan/Projects/personal/liberet-test/backend/icons/megafono.png'
            )
            
            service3 = Service(
                name="Recarga",
                price="0",
                income=True,
                icon_url='/home/ivan/Projects/personal/liberet-test/backend/icons/megafono.png'
            )

            liberet = Supplier(name="Liberet", credits=100)

            session.add_all([service1, service2, service3, liberet])

            session.commit()
        
        return Session(self.engine)


    def drop(self):
        self.engine.execute(f"DROP DATABASE IF EXISTS {self.name}")
        Base.metadata.drop_all(self.engine)
