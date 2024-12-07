import threading
import sqlalchemy
import os

from src.modules.ConfigParser.config_parser import Config
from src.modules.DatabaseModel.database_model import Base

from ..Logger.logger import LogLevel, Logger

class Database:
    _lock = threading.Lock()
    _instance = None
    _engine = None

    def __new__(cls, initialize: bool = False):
        if not initialize:
            assert cls._instance is not None, "Trying to access database before initializing it"
            return cls._instance
        
        with cls._lock:
            if cls._instance == None:
                assert initialize, "Trying to access database without initializing it"
                assert Config._instance is not None, "Trying to initialize database before initialising config"
                assert Config("database") is not None, "No database config!"
                location = Config("database").location
                assert location is not None, "No database location in config file!"
                if not os.path.isfile(location):
                    Logger(f'No .db file found at {location}. Creating a new one...', LogLevel.WARNING)
                    open(location, 'a').close()
                    Logger(f'New file made: {location}', LogLevel.WARNING)
                
                echo_database_output = False
                if Config("database").echo == "True":
                    echo_database_output = True
                cls._instance = super().__new__(cls)
                Logger(f'Initializing database at {location}', LogLevel.INFO)
                cls._engine=sqlalchemy.create_engine(f'sqlite:///{location}', echo=echo_database_output, echo_pool="debug")
                Logger(f'Initializing database at {location}', LogLevel.INFO)
                Base.metadata.create_all(cls._engine)
                
        return cls._instance
    
    @classmethod
    def engine(cls):
        return cls._engine

    def __exit__(self):
         self.engine.dispose()