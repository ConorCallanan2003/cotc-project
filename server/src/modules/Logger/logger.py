import logging
import threading
from enum import Enum
from typing import Literal

class LogLevel(Enum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50
    

class CustomFormatter(logging.Formatter):

    def __init__(self):
        grey = "\x1b[37;20m"
        cyan = "\x1b[36;20m"
        yellow = "\x1b[33;20m"
        red = "\x1b[31;20m"
        bold_red = "\x1b[31;1m"
        reset = "\x1b[0m"
        
        format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
            
        self.formats = {
            logging.DEBUG: cyan + format + reset,
            logging.INFO: grey + format + reset,
            logging.WARNING: yellow + format + reset,
            logging.ERROR: red + format + reset,
            logging.CRITICAL: bold_red + format + reset
        }

    def format(self, record):
        log_fmt = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
    
class Logger():
    
    _instance = None
    _lock = threading.Lock()
    _logger = None
    
    def __new__(cls, message: str = None, level: LogLevel = LogLevel.INFO, intitialize=False, ):
        if cls._instance:
            cls._logger.log(level.value, message)
            return
        assert intitialize, "Attempt to log before logger is initialized! Please initialize the logger with Logger()"
        with cls._lock:
            if cls._instance == None:
                cls._instance = super(Logger, cls).__new__(cls)
                cls._logger = logging.getLogger('main')
                cls._logger.setLevel(logging.DEBUG)
                ch = logging.StreamHandler()

                ch.setFormatter(CustomFormatter())
                

                cls._logger.addHandler(ch)
                cls._logger.debug("Logger initialized")
                
        return cls._instance
    
    @classmethod
    def setLevel(cls, level: str):
        match level:
            case "DEBUG":
                cls._logger.setLevel(logging.DEBUG)
            case "INFO":
                cls._logger.setLevel(logging.INFO)
            case "WARNING":
                cls._logger.setLevel(logging.WARNING)
            case "ERROR":
                cls._logger.setLevel(logging.ERROR)
            case "CRITICAL":
                cls._logger.setLevel(logging.CRITICAL)
            case _:
                cls._logger.setLevel(logging.INFO)
