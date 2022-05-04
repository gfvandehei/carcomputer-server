from pydantic import BaseModel
from typing import List, Optional

class TemperatureSensorDataPoint(BaseModel):
    temperature: float
    humidity: float

class PositionSensorDataPoint(BaseModel):
    gps_network: str
    timestamp: str
    latitude: float
    latitude_direction: str
    longitude: float
    longitude_direction: str
    quality: int
    satalites: int
    horizontal_dilution_of_precision: float
    altitude: float
    altutude_units: str
    geoidal_separation: float
    geoidal_seperation_units: str
    age_of_correction: Optional[float]
    correction_station_id: Optional[str]
    checksum: str

class AccelerometerSensorDataPoint(BaseModel):
    gyro_x: float
    gyro_y: float
    gyro_z: float
    acceleration_x: float
    acceleration_y: float
    acceleration_z: float