import asyncio
from websockets import serve
from src.modules.Logger.logger import LogLevel, Logger
from src.modules.ServerHelpers.server_helpers import ServerHelpers
from src.modules.ArgParser.arg_parser import ArgumentParser
from src.modules.ConfigParser.config_parser import Config
from src.modules.StartUp.start_up import StartUp

async def run_websocket_server():
    from src.websocket_server import connection_manager
    async with serve(connection_manager, "localhost", 8765) as server:
        Logger("WebSocket server started", LogLevel.INFO)
        await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    
    try:
        with StartUp():
            from src.server import App
            run_websocket_server()
            App.run(host=Config("server").host, port=Config("server").port, debug=ArgumentParser().getArg("dev_or_prod"), use_reloader=False)
            
    except Exception as e:
        Logger(e, LogLevel.CRITICAL)
