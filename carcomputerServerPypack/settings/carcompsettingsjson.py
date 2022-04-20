"""
used to generate a carcompsettings object from a json file
"""
import json
from carcomputerServerPypack.settings.carcompsettings import CarcomputerServerSettings

def create_settings_from_json(json_file_path="/etc/carcomputer/conf.json") -> CarcomputerServerSettings:
    json_file_object = open(json_file_path, "r")
    json_file_read: dict = json.load(json_file_object)

    new_config_object = CarcomputerServerSettings()
    new_config_object.redis_host = json_file_read.get("redis_host")
    new_config_object.redis_password = json_file_read.get("redis_password")
    new_config_object.redis_port = json_file_read.get("redis_port")

    return new_config_object