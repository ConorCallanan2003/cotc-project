from src.modules.ArgParser.arg_parser import ArgumentParser
from src.modules.ConfigParser.config_parser import Config
from src.modules.StartUp.start_up import StartUp

if __name__ == "__main__":
    
    # with StartUp() as startup:
    startip = StartUp()
    from src.server import App
    App.run(host=Config("server").host, port=Config("server").port, debug=ArgumentParser().getArg("dev_or_prod"))
    raise Exception("Server failed to start")
