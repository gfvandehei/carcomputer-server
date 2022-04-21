from carcomputerServerPypack.settings.carcompsettingsjson import create_settings_from_json
from carcomputerServerPypack.api.flask_server import create_flask_app

settings_object = create_settings_from_json()
flask_app = create_flask_app(settings_object)

flask_app.run(port=3000)