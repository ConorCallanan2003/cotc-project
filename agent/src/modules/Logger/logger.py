import logging
import threading

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
            logging.INFO: grey + format + reset,
            logging.DEBUG: cyan + format + reset,
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
    
    def __new__(cls, *args, **kwargs):
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
    
    def setLevel(self, level: str):
        logger = self.getLogger()
        match level:
            case "DEBUG":
                logger.setLevel(logging.DEBUG)
            case "INFO":
                logger.setLevel(logging.INFO)
            case "WARNING":
                logger.setLevel(logging.WARNING)
            case "ERROR":
                logger.setLevel(logging.ERROR)
            case "CRITICAL":
                logger.setLevel(logging.CRITICAL)
            case _:
                logger.setLevel(logging.INFO)
        
    def getLogger(cls):
        return cls._logger