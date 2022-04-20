from carcomputerServerPypack.redis.redisInterface import CarComputerRedisInterface
from carcomputerServerPypack.settings.carcompsettingsjson import create_settings_from_json

settings = create_settings_from_json()
redis_interface = CarComputerRedisInterface(settings)

# create some fake sensor
redis_interface.xadd("sensor:myfakesensor:log", {
    "value1": 1,
    "value2": 2,
    "value3": 3
})
sensors = set(redis_interface.query_sensor_names())
assert("myfakesensor" in sensors)

values = redis_interface.get_sensor_data_values("myfakesensor")
print(values)

redis_interface.xtrim("sensor:myfakesensor:log", 0)
redis_interface.delete("sensor:myfakesensor:log")