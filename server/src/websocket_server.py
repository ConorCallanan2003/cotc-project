from websockets.asyncio.server import ServerConnection
from src.modules.WebSocketQueue.websocket_queue import WebSocketConnectionManager


async def connection_manager(websocket: ServerConnection):
    try:
        
        connection_details = await websocket.recv()
        breakpoint()
        # Register user
        WebSocketConnectionManager.add_client(websocket)
        # broadcast(USERS, users_event())
        # Send current state to user
        # await websocket.send(value_event())
        # Manage state changes
        # async for message in websocket:
        #     event = json.loads(message)
        #     if event["action"] == "minus":
        #         VALUE -= 1
        #         broadcast(USERS, value_event())
        #     elif event["action"] == "plus":
        #         VALUE += 1
        #         broadcast(USERS, value_event())
        #     else:
        #         logging.error("unsupported event: %s", event)
    finally:
        # Unregister user
        print("Unregistering user")
        # USERS.remove(websocket)
        # broadcast(USERS, users_event())
        