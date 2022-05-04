from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class Sensor(Base):
    __tablename__="sensor"
    
    sensor_name = Column(String, primary_key=True)
    sensor_type = Column(String, ForeignKey("sensortype.name")) # links to sensor_types table
    sensor_position = Column(String, ForeignKey("carposition.name")) # links to car position table
    sample_rate = Column(Integer)

class SensorModel(BaseModel):
    sensor_name: str
    sensor_type: str
    sensor_position: str
    sample_rate: int

    class Config:
        orm_mode = True

class SensorType(Base):
    __tablename__="sensortype"
    
    name = Column(String, primary_key=True)

class SensorTypeModel(BaseModel):
    name: str

    class Config:
        from_orm = True

class CarPosition(Base):
    __tablename__="carposition"

    name = Column(String, primary_key=True)
    x = Column(Integer)
    y = Column(Integer)

class CarPositionModel(BaseModel):
    name: str
    x: int
    y: int

    class Config:
        from_orm = True
