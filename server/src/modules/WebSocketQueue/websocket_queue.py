class WebSocketDispatchManager:
    sender_funcs: dict[int, list[callable]] = {}
    
    def __init__(self, device_type_id, sender):
        if device_type_id not in WebSocketDispatchManager.sender_funcs.keys() and WebSocketDispatchManager.sender_funcs[device_type_id]:
            WebSocketDispatchManager.sender_funcs[device_type_id].append(sender)
    
    @staticmethod
    def call(device_type_id, data):
        sender = WebSocketDispatchManager.sender_funcs[device_type_id]
        if sender is not None:
            sender(data)
        
    def __del__(self):
        if self.device_type_id in self.sender_funcs.keys():
            del self.sender_funcs[str(self.device_type_id)]
    