import math
from random import randint
from carcomputerServerPypack.database.sqlite import create_database_connection
from carcomputerServerPypack.settings.carcompsettingsjson import create_settings_from_json
import carcomputerServerPypack.database.model as Model
from sqlalchemy.orm import Session
import redis
import time

settings_object = create_settings_from_json()
sessionmaker = create_database_connection(settings=settings_object)


session: Session = sessionmaker()
# this should be commented out
front_position = session.query(Model.CarPosition).filter(Model.CarPosition.name=="front bumper").one_or_none()
if front_position is None:
    front_position = Model.CarPosition()
    front_position.name = "front bumper"
    front_position.x = 0
    front_position.y = 0
    session.add(front_position)

interior_position = session.query(Model.CarPosition).filter(Model.CarPosition.name=="under dashboard").one_or_none()
if interior_position is None:
    interior_position = Model.CarPosition()
    interior_position.name = "under dashboard"
    interior_position.x = 30
    interior_position.y = 0
    session.add(interior_position)

new_sensor_type = session.query(Model.SensorType).filter(Model.SensorType.name=="climate").one_or_none()
if new_sensor_type is None:
    new_sensor_type = Model.SensorType()
    new_sensor_type.name = "climate"
    session.add(new_sensor_type)
# check to see if test object already exists
inclimate = session.query(Model.Sensor).filter(Model.Sensor.sensor_name=="interior-climate").one_or_none()
outclimate = session.query(Model.Sensor).filter(Model.Sensor.sensor_name=="exterior-climate").one_or_none()

if inclimate is None:
    new_in_climate = Model.Sensor()
    new_in_climate.sample_rate = 1
    new_in_climate.sensor_name = "interior-climate"
    new_in_climate.sensor_position = "front bumper"
    new_in_climate.sensor_type = "climate"
    session.add(new_in_climate)

if outclimate is None:
    new_in_climate = Model.Sensor()
    new_in_climate.sample_rate = 1
    new_in_climate.sensor_name = "exterior-climate"
    new_in_climate.sensor_position = "under dashboard"
    new_in_climate.sensor_type = "climate"
    session.add(new_in_climate)

session.commit()
session.close()

## now add sensor data to redis periodically

redis_interface = redis.Redis(settings_object.redis_host, settings_object.redis_port)
redis_interface.xadd("sensor:exterior-climate:state", {
    "state": "ACTIVE"
})
redis_interface.xadd("sensor:interior-climate:state", {
    "state": "ACTIVE"
})

try:
    print("Starting to add to sensor test_climate_frontbump stream")
    while True:
        redis_interface.xadd("sensor:exterior-climate:log", {
            "temperature": randint(65, 100),
            "humidity": randint(50, 55)
        })
        redis_interface.xadd("sensor:interior-climate:log", {
            "temperature": randint(65, 100),
            "humidity": randint(50, 55)
        })
        time.sleep(1) # periodicity of 1 second as defined above
except KeyboardInterrupt:
    # shutdown redis stuff
    redis_interface.xadd("sensor:exterior-climate:state", {
        "state": "INACTIVE"
    })
    redis_interface.xadd("sensor:interior-climate:state", {
        "state": "INACTIVE"
    })
    """print("deleting redis streams for test sensor due to keyboard interupt")
    redis_interface.xtrim("sensor:exterior-climate:log", 0)
    redis_interface.delete("sensor:exterior-climate:log")
    print("deleting redis streams for test sensor due to keyboard interupt")
    redis_interface.xtrim("sensor:interior-climate:log", 0)
    redis_interface.delete("sensor:interior-climate:log")"""
    