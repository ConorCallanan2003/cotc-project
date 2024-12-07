print("IMPORTED") 
from flask import Flask, request, jsonify
from sqlalchemy.orm import Session
from src.modules.DatabaseModel.database_model import Base, Device, Aggregator

from src.modules.ServerHelpers.server_helpers import ServerHelpers
from src.modules.Logger.logger import LogLevel, Logger
import time

arg_parser = None
logger = None
engine = None

App = Flask(__name__)

@App.errorhandler(404)
def not_found(error):
    Logger(f"Route not found: {request.url}", LogLevel.INFO)
    return jsonify({'error': 'Route not found'}), 404


@App.get("/hello_world")
def hello_world():
    return "<p>Hello, World!</p>"


@App.get("/test_resource_heavy_request")
@ServerHelpers.timer
def test_resource_heavy_request():
    time.sleep(5)
    return "<p>Hello, World!</p>"


@App.post("/register_device")
@ServerHelpers.session_provider
@ServerHelpers.timer
def create_user(session: Session):
    data = request.get_json()
    session.add(Aggregator(guid=data["guid"], name=data["name"]))
    return "<p>User created!</p>"
