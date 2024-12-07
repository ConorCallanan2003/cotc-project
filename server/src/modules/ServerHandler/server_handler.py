# from ..StartUp.start_up import StartUp
# import threading

# class ServerThread(threading.Thread):
#     _instance = None
#     _lock = threading.Lock()

#     def __new__(cls, *args, **kwargs):
#         with cls._lock:
#             if cls._instance is None:
#                 cls._instance = super(ServerThread, cls).__new__(cls)
#             return cls._instance

#     def __init__(self, app="server:app", host="0.0.0.0", port=8000):
#         assert self.__class__._instance != None, "ServerThread class created incorrectly"
#         self.app = app
#         self.host = host
#         self.port = port

#     def serve(self):
#         with StartUp() as startup:
#             logger = startup.getLogger()

#             logger.debug("About to run server")
#             uvicornConfig = startup.getUvicornConfig()

#             logger.debug("Retrieved server config")

#             server_thread = threading.Thread(
#                 target=,
#                 args=(self.app,),
#                 kwargs={
#                     "host": self.host,
#                     "port": self.port,
#                     **uvicornConfig
#                 }
#             )

#             server_thread.start()

#             self

#             logger.info("Server is running")
