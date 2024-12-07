import threading
import sqlalchemy
from ..Logger.logger import LogLevel, Logger

class Database:
    _lock = threading.Lock()
    _instance = None
    _engine = None

    def __new__(cls, location: str):
        with cls._lock:
            if cls._instance == None:
                cls._instance = super().__new__(cls)
                Logger(f'Initializing database at {location}', LogLevel.INFO)
                cls._engine=sqlalchemy.create_engine(f'sqlite:///{location}')
                
        return cls._instance
    
    @classmethod
    def engine(cls):
        return cls._engine

    def __exit__(self):
         self.engine.dispose()