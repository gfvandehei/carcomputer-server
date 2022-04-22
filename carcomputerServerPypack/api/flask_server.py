import flask
from carcomputerServerPypack.database.sqlite import create_database_connection
from carcomputerServerPypack.redis.redisInterface import CarComputerRedisInterface
from carcomputerServerPypack.settings.carcompsettings import CarcomputerServerSettings

import carcomputerServerPypack.api.blueprints.sensor as SensorBP

def create_flask_app(settings: CarcomputerServerSettings):
    flask_app = flask.Flask(__name__, static_url_path="/", static_folder="/home/gfvandehei/Documents/carcomputer-dev/carcomputer-server/static")

    # create supporting objets
    db_session_maker = create_database_connection(settings)
    redis_connection = CarComputerRedisInterface(settings)

    # create blueprints
    sensor_blueprint = SensorBP.create_blueprint(redis_connection, db_session_maker)
    flask_app.register_blueprint(sensor_blueprint, url_prefix="/sensors")

    @flask_app.route("/")
    def index():
        return flask.redirect("/index.html")
    return flask_app