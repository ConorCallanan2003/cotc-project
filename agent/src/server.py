from fastapi import FastAPI
from contextlib import asynccontextmanager
from modules.Logger.logger import Logger


logger = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global logger
    loggerWrapper = Logger()
    logger = loggerWrapper.getLogger()
    logger.info("Logger aquired by server")
    yield
    logger.info("Shutting down...")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    logger.info("Hello World called!")
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/users/me")
def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
def read_user(user_id: str):
    return {"user_id": user_id}

@app.get("/users/{user_id}/items/{item_id}")
def read_user_item(user_id: int, item_id: str, q: str = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
