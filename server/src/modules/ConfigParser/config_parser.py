import threading 
import configparser
from ..Logger.logger import LogLevel, Logger

class Config():
    
    _instance = None
    _config = None
    _lock = threading.Lock()
    
    def __new__(cls, section: str = None, path: str = "config.ini"):
        if section is not None:
            if not cls._config.has_section(section):
                if Logger._instance != None:
                    Logger(f"Config section \"{section}\" does not exist", LogLevel.CRITICAL)
                else:
                    print(f"Config section {section} does not exist")
                return False
            return Option(dict(cls._config.items(section)))
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._initialize(path)
                
        return cls._instance
    
    @classmethod
    def _initialize(cls, path: str = "config.ini"):
        if cls._config is None:
            config = configparser.ConfigParser()
            config.read(path)
            cls._config = config
            
    @classmethod
    def _sections(cls):
        return {section: dict(cls._config[section]) for section in cls._config.sections()}

    # @classmethod
    # def __getattr__(cls, section):
    #     if not cls._config.has_section(section):
    #         if Logger._instance != None:
    #             Logger(f"Config section \"{section}\" does not exist", LogLevel.CRITICAL)
    #         else:
    #             print(f"Config section {section} does not exist")
    #         return False
    #     return dict(cls._config.items(section))


class Option():
    
    def __init__(self, section_dict: dict):
         self.section_dict = section_dict
         
    def __getattr__(self, option):
        if option not in self.section_dict:
            if Logger._instance != None:
                Logger(f"Config option \"{option}\" does not exist", LogLevel.CRITICAL)
            else:
                print(f"Config option {option} does not exist")
            return False
        return self.section_dict[option]