from flask import Blueprint, request, jsonify, Response
from typing import List
from carcomputerServerPypack.redis.redisInterface import CarComputerRedisInterface
import carcomputerServerPypack.database.model as Model
from sqlalchemy.orm import sessionmaker, Session

def create_blueprint(
        redis_interface: CarComputerRedisInterface,
        sessionmaker: sessionmaker
    ) -> Blueprint:

    sensor_blueprint = Blueprint("sensor", __name__)

    @sensor_blueprint.route("/")
    def list_sensors():
        # query database for all sensors
        session: Session = sessionmaker()
        sensors = session.query(Model.Sensor).all()
        session.close()
        print(sensors)
        # query params type=?, position=?
        # return all json objects for sensors, not including values
        return {
            "data": sensors
        }

    @sensor_blueprint.route("/<sensor_name>")
    def get_sensor_value(sensor_name):
        try:
            session: Session = sessionmaker()
            sensor_db_object: Model.Sensor = session.query(Model.Sensor).filter(Model.Sensor.sensor_name==sensor_name).one()
            session.close()
            sensor_data = {
                "metadata": sensor_db_object, # replace with serialized database object
                "state": redis_interface.get_sensor_current_state(sensor_name),
                "data": redis_interface.get_sensor_data_values(sensor_name)
            }
            print(sensor_data)
            return {
                "data": sensor_data
            }
        except Exception as err:
            print(err)
            return Response(str(err), 404)

    return sensor_blueprint

