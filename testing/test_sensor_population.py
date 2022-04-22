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
new_position = session.query(Model.CarPosition).filter(Model.CarPosition.name=="front bumper").one_or_none()
if new_position is None:
    new_position = Model.CarPosition()
    new_position.name = "front bumper"
    new_position.x = 0
    new_position.y = 0
    session.add(new_position)

new_sensor_type = session.query(Model.SensorType).filter(Model.SensorType.name=="climate").one_or_none()
if new_sensor_type is None:
    new_sensor_type = Model.SensorType()
    new_sensor_type.name = "climate"
    session.add(new_position)
# check to see if test object already exists
sensor_existing: Model.Sensor = session.query(Model.Sensor).filter(Model.Sensor.sensor_name=="test_climate_frontbump").one_or_none()
print(sensor_existing)
if sensor_existing:
    # delete it
    session.delete(sensor_existing)
    session.commit()
new_test_sensor = Model.Sensor()
new_test_sensor.sample_rate = 1
new_test_sensor.sensor_name = "test_climate_frontbump"
new_test_sensor.sensor_position = new_position.name
new_test_sensor.sensor_type = new_sensor_type.name
session.add(new_test_sensor)
session.commit()

session.close()

## now add sensor data to redis periodically

redis_interface = redis.Redis(settings_object.redis_host, settings_object.redis_port)
redis_interface.xadd("sensor:test_climate_frontbump:state", {
    "state": "ACTIVE"
})

try:
    print("Starting to add to sensor test_climate_frontbump stream")
    while True:
        redis_interface.xadd("sensor:test_climate_frontbump:log", {
            "temperature": randint(65, 100),
            "humidity": randint(50, 55)
        })
        time.sleep(1) # periodicity of 1 second as defined above
except KeyboardInterrupt:
    # shutdown redis stuff
    print("deleting redis streams for test sensor due to keyboard interupt")
    redis_interface.xtrim("sensor:myfakesensor:log", 0)
    redis_interface.delete("sensor:myfakesensor:log")
    