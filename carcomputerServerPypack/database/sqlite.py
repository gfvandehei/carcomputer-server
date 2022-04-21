from importlib import resources
import sqlite3
from carcomputerServerPypack.settings.carcompsettings import CarcomputerServerSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from carcomputerServerPypack.database.model import Base

def create_database_connection(settings: CarcomputerServerSettings):
    engine = create_engine(f"sqlite:///{settings.sqlite_file}")
    Session = sessionmaker()
    Session.configure(bind=engine)

    Base.metadata.create_all(engine)
    return Session