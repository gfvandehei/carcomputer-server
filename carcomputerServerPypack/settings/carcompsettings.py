class CarcomputerServerSettings(object):
    redis_host: str
    redis_port: int = None
    redis_password: str = None
    sqlite_file: str = "/etc/carcomputer/data/sqlite.db"