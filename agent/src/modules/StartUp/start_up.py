import logging
from modules.ArgParser.arg_parser import ArgumentParser
from modules.ConfigParser.config_parser import ConfigParser
from modules.Logger.logger import Logger

class StartUp():
    def __enter__(self):
        print("Starting logger...")
        loggerWrapper = Logger()
        logger = loggerWrapper.getLogger()
        assert type(logger) == logging.Logger, "logger variable is not of type logging.Logger"
        logger.info("Logger started")
        logger.info("Parsing args...")
        parser = ArgumentParser()
        parser.add_argument("dev_or_prod", type=str, help="Specify whether to run in development or production mode", choices=["dev", "prod"])
        parser.add_optional_argument("config_file", type=str, help="The path to the config file")

        args = parser.parse_args()
        logger.info("Args parsed")
        logger.info("Parsing config...")

        if args.config_file == None:
            args.config_file = f"../config/config_{args.dev_or_prod}.ini"

        config = ConfigParser(args.config_file)

        logger.info("Config parsed")

        logger.info("Configuring logging")

        if config.logging and config.logging.level:
            self.logLevel = config.logging.level
            loggerWrapper.setLevel(config.logging.level)

        logger.info("Logging configured")

        logger.debug("Debug log level enabled")
        logger.warning("Warning log level enabled")
        logger.error("Error log level enabled")
        logger.critical("Critical log level enabled")

        config.setLogger(logger)

        self.config = config
        self.logger = logger

    def __setUpUvicornConfigForLogs__(self):
        config = {}

        # this is default (site-packages\uvicorn\main.py)
        config['log_config'] = {
        "version":1,
        "disable_existing_loggers": True,
        "formatters":{
            "default":{
                "()":"uvicorn.logging.DefaultFormatter",
                "fmt":"%(levelprefix)s %(message)s",
                "use_colors":"None"
            },
            "access":{
                "()":"uvicorn.logging.AccessFormatter",
                "fmt":"%(levelprefix)s %(client_addr)s - \"%(request_line)s\" %(status_code)s"
            }
        },
        "handlers":{
            "default":{
                "formatter":"default",
                "class":"logging.StreamHandler",
                "stream":"ext://sys.stderr"
            },
            "access":{
                "formatter":"access",
                "class":"logging.StreamHandler",
                "stream":"ext://sys.stdout"
            }
        },
        "loggers":{
            "uvicorn":{
                "handlers":[
                    "default"
                ],
                "level":"INFO"
            },
            "uvicorn.error":{
                "level":"INFO",
                "handlers":[
                    "default"
                ],
                "propagate": True
            },
            "uvicorn.access":{
                "handlers":[
                    "access"
                ],
                "level":"INFO",
                "propagate": False
            }
        }
        }

        # add your handler to it (in my case, I'm working with quart, but you can do this with Flask etc. as well, they're all the same)
        config['log_config']['loggers']['quart'] = {
        "handlers":[
            "default"
        ],
        "level": self.logLevel
        }

        self.uvicornConfig = config

    def getUvicornConfig(self):
        return self.uvicornConfig

    def getLogger(self) -> logging.Logger:
        assert type(self.logger) == logging.Logger, "logger variable is not of type logging.Logger"
        return self.logger

    def getLogLevel(self):
        return self.logLevel

    def __exit__(self, exc_type, exc_val, exc_tb):
        assert type(self.logger) == logging.Logger, "logger variable is not of type logging.Logger"
        self.logger.info("Exiting program and releasing resources...")
        for handler in self.logger.handlers:
            handler.close()
            self.logger.removeHandler(handler)
        self.logger = None
        self.loggerWrapper = None
        self.parser = None
        self.config = None
        self.args = None
        return True


if __name__ == "__main__":

    startUp = StartUp()
    logger = startUp.getLogger()

    assert(type(logger) == logging.Logger)

    logger.info("Startup complete")
