""" Database Settings """

from masonite.environment import LoadEnvironment, env


"""
|--------------------------------------------------------------------------
| Load Environment Variables
|--------------------------------------------------------------------------
|
| Loads in the environment variables when this page is imported.
|
"""

LoadEnvironment()

"""
|--------------------------------------------------------------------------
| Database Settings
|--------------------------------------------------------------------------
|
| Set connection database settings here as a dictionary. Follow the
| format below to create additional connection settings.
|
| @see Orator migrations documentation for more info
|
"""

DATABASES = {
    "default": env('DB_DRIVER'),
    "mysql": {
        "driver": "mysql",
        "host": env("MYSQL_DATABASE_HOST"),
        "user": env("MYSQL_DATABASE_USER"),
        "password": env("MYSQL_DATABASE_PASSWORD"),
        "database": env("MYSQL_DATABASE_DATABASE"),
        "port": env("MYSQL_DATABASE_PORT"),
        "prefix": "",
        "grammar": "mysql",
        "options": {
            "charset": "utf8mb4",
        },
        "log_queries": True,
    },
    "postgres": {
        "driver": "postgres",
        "host": env("DB_HOST"),
        "user": env("DB_USERNAME"),
        "password": env("DB_PASSWORD"),
        "database": env("DB_DATABASE"),
        "port": env("DB_PORT"),
        "prefix": "",
        "log_queries": True,
    },
    "sqlite": {
        "driver": "sqlite",
        "database": env("DB_DATABASE"),
        "prefix": "",
        "log_queries": True,
    },
    "mssql": {
        "driver": "mssql",
        "host": env("MSSQL_DATABASE_HOST"),
        "user": env("MSSQL_DATABASE_USER"),
        "password": env("MSSQL_DATABASE_PASSWORD"),
        "database": env("MSSQL_DATABASE_DATABASE"),
        "port": env("MSSQL_DATABASE_PORT"),
        "prefix": "",
        "log_queries": True,
    },
}

try:
    from masoniteorm.connections import ConnectionResolver
    DB = ConnectionResolver().set_connection_details(DATABASES)
except:
    from orator import DatabaseManager, Model
    DB = DatabaseManager(DATABASES)
    Model.set_connection_resolver(DB)