from ..StartUp.start_up import StartUp
import uvicorn

class Server():
    def __init__(self, app="server:app", host="0.0.0.0", port=8000):
        self.app = app
        self.host = host
        self.port = port
        
    def serve(self):
        with StartUp():
            print("HERE")
            # logger = startup.getLogger()
            print("HERE 2")
            # env = startup.getEnv()
            # uvicornConfig = startup.getUvicornConfig()
            
            # logger.info("About to run server")
            
            uvicorn.run(self.app, host=self.host, port=self.port)
            
            # logger.info("Server is running")