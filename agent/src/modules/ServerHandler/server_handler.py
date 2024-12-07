from ..StartUp.start_up import StartUp
import uvicorn

class Server():
    def __init__(self, app="server:app", host="0.0.0.0", port=8000):
        self.app = app
        self.host = host
        self.port = port

    def serve(self):
        with StartUp():
            # env = startup.getEnv()
            # uvicornConfig = startup.getUvicornConfig()
            uvicorn.run(self.app, host=self.host, port=self.port)
