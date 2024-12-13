import inspect
import os
import traceback
from src.modules.ServerHelpers.server_helpers import ServerHelpers
from src.modules.Database.database import Database

# Code to be run during server startup
if __name__ == "__main__":
    dir_path = '../../'
    absolute_path = os.path.abspath(dir_path)
    existing_path = os.environ.get('PATH')

    os.environ['PATH'] = dir_path + ':' + absolute_path

    print(absolute_path)

from src.modules.ArgParser.arg_parser import ArgumentParser
from src.modules.ConfigParser.config_parser import Config
from src.modules.Logger.logger import LogLevel, Logger

class StartUp():
    def __enter__(self):
    # def __init__(self):
        print("Starting logger...")
        Logger(intitialize=True)
        
        Logger("Logger started", LogLevel.INFO)
        Logger("Parsing args...", LogLevel.INFO)
        
        ArgumentParser()
        ArgumentParser().add_argument("dev_or_prod", arg_type=str, help="Specify whether to run in development or production mode", choices=["dev", "prod"])
        ArgumentParser().add_optional_argument("config_file", arg_type=str, help="The path to the config file")

        ArgumentParser.parseArgs()
        
        Logger("Args parsed", LogLevel.INFO)
        Logger("Parsing config...", LogLevel.INFO)

        assert type(ArgumentParser().getArg("config_file")) == str, "No config file provided! Please provide a config file in command line args"
        assert os.path.isfile(ArgumentParser().getArg("config_file")), "Config file does not exist"
            
        Config(path=ArgumentParser().getArg("config_file"))

        Logger(f"Config parsed! Parsed: {Config._sections()}", LogLevel.INFO)
        
        Logger("Configuring database...", LogLevel.INFO)
        assert Config("database").location, "No database location provided in config file"
        
        Database(initialize=True)
        Logger("Database configured", LogLevel.INFO)

        Logger("Configuring logging", LogLevel.INFO)    

        if Config("logging"):
            Logger.setLevel(Config("logging").level)

        Logger("Logging configured", LogLevel.INFO)
        
        Logger("Initializing server helpers...", LogLevel.INFO)
        ServerHelpers.initialize()
        Logger("Servers helpers initialized", LogLevel.INFO)

        Logger("Debug log level enabled", LogLevel.DEBUG)
        Logger("Warning log level enabled", LogLevel.WARNING)
        Logger("Error log level enabled", LogLevel.ERROR)
        Logger("Critical log level enabled", LogLevel.CRITICAL)
        
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        Logger("Exiting program and releasing resources...", LogLevel.INFO)
        self.parser = None
        self.config = None
        self.args = None
        if exc_type:
            exc_info = traceback.format_exception(exc_type, value=exc_val, tb=exc_tb)
            for line in exc_info:
                Logger(line.strip(), LogLevel.ERROR)

        else:
            Logger("Exiting program successfully", LogLevel.INFO)
        Logger("Program exited", LogLevel.INFO)
        return True


if __name__ == "__main__":

    startUp = StartUp()

    Logger("Startup complete", LogLevel.INFO)
