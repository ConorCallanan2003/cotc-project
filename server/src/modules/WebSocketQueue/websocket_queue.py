from src.modules import Logger
from src.modules.Logger.logger import LogLevel


class WebSocketConnectionManager:
    sender_funcs: dict[int, dict[str, list[callable]]] = {}
    
    @staticmethod
    def add_client(device_type_id, session_id, func):
        if device_type_id not in WebSocketConnectionManager.sender_funcs.keys():
            WebSocketConnectionManager.sender_funcs[str(device_type_id)] = {}
        
        if str(session_id) not in WebSocketConnectionManager.sender_funcs[str(device_type_id)].keys():
            WebSocketConnectionManager.sender_funcs[str(device_type_id)][str(session_id)] = func
            
        Logger(f"Client {session_id} subscribed to device with ID {device_type_id}", LogLevel.INFO)
    
    @staticmethod
    def call(device_type_id, data):
        funcs = WebSocketConnectionManager.sender_funcs[device_type_id]
        
        for sender in funcs.values():
            sender(data)
          
    @staticmethod  
    def remove_client(device_type_id, session_id):
        for device_type_id in WebSocketConnectionManager.sender_funcs.keys():
            if str(session_id) in WebSocketConnectionManager.sender_funcs[device_type_id].keys():
                del WebSocketConnectionManager.sender_funcs[device_type_id][str(session_id)]
    