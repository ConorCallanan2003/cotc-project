from src.modules.ServerHelpers.server_helpers import ServerHelpers
from src.modules.ArgParser.arg_parser import ArgumentParser
from src.modules.ConfigParser.config_parser import Config
from src.modules.StartUp.start_up import StartUp

if __name__ == "__main__":
    
    with StartUp():
        from src.server import App
        App.run(host=Config("server").host, port=Config("server").port, debug=ArgumentParser().getArg("dev_or_prod"), use_reloader=False)
    raise Exception("Server failed to start")
