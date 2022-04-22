import redis
import datetime
from carcomputerServerPypack.settings.carcompsettings import CarcomputerServerSettings

def nobytestring(value):
    if isinstance(value, bytes):
        return value.decode("utf-8")
    else:
        return value

class CarComputerRedisInterface(redis.Redis):

    def __init__(self, carcomp_settings: CarcomputerServerSettings):
        super().__init__(
            carcomp_settings.redis_host,
            carcomp_settings.redis_port,
            0,
            carcomp_settings.redis_password)
        
    def query_sensor_names(self):
        names = []
        for key in self.scan_iter("sensor:*"):
            key: str = key.decode("utf-8")
            # parse out just the name
            # sensor streams are in the form sensor:<name>:<streamname>
            sensor_name = key.split(":")[1]
            names.append(sensor_name)
        return names
    
    def get_sensor_data_values(self, sensor_name, how_many=100):
        sensor_data = self.xrevrange(f"sensor:{sensor_name}:log", count=how_many)
        sensor_data_parsed = []
        for data_point in sensor_data:
            # parse the sensor data
            timestamp_str = int(data_point[0].decode("utf-8").split("-")[0])
            timestamp = datetime.datetime.fromtimestamp(timestamp_str/1000) # converts from ms to s
            data_dict: dict = data_point[1]
            data_nobytekeys = {key.decode(): nobytestring(value) for key, value in data_dict.items()}
            sensor_data_parsed.append({
                "timestamp": timestamp,
                "data": data_nobytekeys
            })
        return sensor_data_parsed

    def get_sensor_state_history(self, sensor_name, how_many=100):
        sensor_data = self.xrange(f"sensor:{sensor_name}:state", count=how_many)
        sensor_data_parsed = []
        for data_point in sensor_data:
            # parse the sensor data
            timestamp_str = int(data_point[0].decode("utf-8").split("-")[0])
            timestamp = datetime.datetime.fromtimestamp(timestamp_str/1000) # converts from ms to s
            data_dict: dict = data_point[1]
            data_nobytekeys = {key.decode(): nobytestring(value) for key, value in data_dict.items()}
            sensor_data_parsed.append({
                "timestamp": timestamp,
                "state": data_nobytekeys
            })
        return sensor_data_parsed
    
    def get_sensor_current_state(self, sensor_name):
        sensor_data = self.xrevrange(f"sensor:{sensor_name}:state", count=1)
        try:
            data_point = sensor_data[0]
            timestamp_str = int(data_point[0].decode("utf-8").split("-")[0])
            timestamp = datetime.datetime.fromtimestamp(timestamp_str/1000) # converts from ms to s
            data_dict: dict = data_point[1]
            
            data_nobytekeys = {key.decode(): nobytestring(value) for key, value in data_dict.items()}
            return {
                "timestamp": timestamp,
                "state": data_nobytekeys
            }
        except Exception as err:
            return str(err)