import functools
import time
from sqlalchemy.orm import Session
from src.modules.Database.database import Database
from src.modules.Logger.logger import LogLevel, Logger

class ServerHelpers:
    engine = None
    
    @staticmethod
    def initialize():
       ServerHelpers.engine = Database().engine() 
    
    @staticmethod
    def timer(func):
        @functools.wraps(func)
        def decorated_function(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            Logger(f"Route {func.__name__} took {elapsed_time} seconds to execute.", LogLevel.DEBUG)
            return result
        return decorated_function
    
    @staticmethod
    def session_provider(func):
        @functools.wraps(func)
        def decorated_function(*args, **kwargs):
            with Session(ServerHelpers.engine) as session:
                result = func(session, *args, **kwargs)
                session.commit()
                return result
        return decorated_function
    
    def __del__(self):
        del self.engine