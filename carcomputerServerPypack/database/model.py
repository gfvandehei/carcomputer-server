from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

@dataclass
class Sensor(Base):
    __tablename__="sensor"
    
    sensor_name = Column(String, primary_key=True)
    sensor_type = Column(String, ForeignKey("sensortype.name")) # links to sensor_types table
    sensor_position = Column(String, ForeignKey("carposition.name")) # links to car position table
    sample_rate = Column(Integer)

@dataclass
class SensorType(Base):
    __tablename__="sensortype"
    
    name = Column(String, primary_key=True)

@dataclass
class CarPosition(Base):
    __tablename__="carposition"

    name = Column(String, primary_key=True)
    x = Column(Integer)
    y = Column(Integer)
