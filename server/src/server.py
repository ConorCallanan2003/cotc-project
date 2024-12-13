from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_socketio import SocketIO, emit, join_room
from flask_cors import CORS
from sqlalchemy.orm import Session
from src.modules.ArgParser.arg_parser import ArgumentParser
from src.modules.DatabaseModel.database_model import *
from datetime import datetime, timezone

from src.modules.ServerHelpers.server_helpers import ServerHelpers
from src.modules.Logger.logger import LogLevel, Logger
import time

App = Flask(__name__)
CORS(App)
socketio = SocketIO(App, cors_allowed_origins="*")

@socketio.on('connect')
def connect():
    Logger(f"Client connected: {request.sid}", LogLevel.INFO)

@socketio.on('subscribe')
@ServerHelpers.session_provider
def subscribe(session: Session, data):
    data_to_date: MetricSnapshot = session.query(MetricSnapshot).filter(MetricSnapshot.metric_type_id == data['metric_id']).order_by(MetricSnapshot.client_timestamp_utc.desc()).limit(200).all()
    Logger(f"Sending data to date for metric {data["metric_id"]} to session {request.sid}", LogLevel.DEBUG)
    emit("initial_data", [{"timestamp": str(int(datetime.strptime(x.client_timestamp_utc, '%Y-%m-%dT%H:%M:%S').timestamp() * 1000)), "value": int(x.value)} for x in data_to_date])
    Logger(f"Attempting to add session {request.sid} to socketio room of metric {data['metric_id']}", LogLevel.DEBUG)
    join_room(data['metric_id'])
    Logger(f"Successfully added session {request.sid} to socketio room of metric {data['metric_id']}", LogLevel.DEBUG)
    

@socketio.on('disconnect')
def disconnect():
    Logger(f"Client disconnected: {request.sid}", LogLevel.INFO)
    # WebSocketConnectionManager.remove_client(device_id, request.sid)
    
# @App.route('/')
# def home():
#     """Renders the home page."""
#     return render_template('index.html')

@App.get("/favicon.ico")
def favicon():
    return send_from_directory('static', "favicon.ico")

@App.errorhandler(404)
def not_found():
    Logger(f"Route not found: {request.url}", LogLevel.WARNING)
    return jsonify({'error': 'Route not found'}), 404

@App.errorhandler(Exception)
def generic_error_handler(error):
    Logger(f"Internal error: {error}", LogLevel.ERROR)
    return jsonify({'error': 'Internal error'}), 500


@App.get("/aggregators")
@ServerHelpers.session_provider
def get_aggregators(session: Session):
    aggregators = session.query(Aggregator).all()
    return jsonify([x.to_dict() for x in aggregators])

@App.get("/aggregator/<id>")
@ServerHelpers.session_provider
def get_aggregator(session: Session, id):
    aggregator = session.query(Aggregator).get(id)
    return jsonify(aggregator.to_dict())

@App.get("/devices")
@ServerHelpers.session_provider
def get_devices(session: Session):
    aggregator_id = request.args.get('aggregator_id')
    if aggregator_id:
        devices = session.query(Device).filter(Device.aggregator_id == aggregator_id).all()
        return jsonify([device.to_dict() for device in devices])
    devices = session.query(Device).all()
    return jsonify([device.to_dict() for device in devices])

@App.get("/device/<id>")
@ServerHelpers.session_provider
def get_device(session: Session, id):
    device = session.query(Device).get(id)
    return jsonify(device.to_dict())

@App.get("/metrics")
@ServerHelpers.session_provider
def get_metrics(session: Session):
    device_id = request.args.get('device_id')
    if device_id:
        metrics = session.query(MetricType).filter(MetricType.device_id == device_id).all()
        return jsonify([metric.to_dict() for metric in metrics])
    metrics = session.query(MetricType).all()
    return jsonify([metric.to_dict() for metric in metrics])

@App.get("/metric/<id>")
@ServerHelpers.session_provider
def get_metric(session: Session, id):
    metric_type = session.query(MetricType).get(id)
    return jsonify(metric_type.to_dict())

@App.get("/test_resource_heavy_request")
@ServerHelpers.timer
def test_resource_heavy_request():
    time.sleep(5)
    return "<p>Hello, World!</p>"

@App.post("/register/aggregator")
@ServerHelpers.timer
@ServerHelpers.session_provider
def register_aggregator(session: Session):
    data = request.get_json()
    aggregator = Aggregator(name=data["name"], mac_address=data["mac_address"])
    session.add(aggregator)
    session.flush()
    return jsonify({'message': f"Aggregator '{aggregator.name}' registered!", 'id': aggregator.id}), 201


@App.post("/register/device")
@ServerHelpers.timer
@ServerHelpers.session_provider
def register_device(session: Session):
    data = request.get_json()
    device = Device(aggregator_id=data['aggregator_id'], name=data['name'], mac_address=data['mac_address'])
    session.add(device)
    session.flush()
    return jsonify({'message': f"Device '{device.name}' registered!", 'id': device.id}), 201


@App.post("/register/metric_type")
@ServerHelpers.timer
@ServerHelpers.session_provider
def register_metric_type(session: Session):
    data = request.get_json()
    metric_type = MetricType(device_id=data['device_id'], name=data['name'])
    session.add(metric_type)
    session.flush()
    return jsonify({'message': f"Metric type '{metric_type.name}' registered!", 'id': metric_type.id}), 201


@App.post("/post/metric_snapshot")
@ServerHelpers.timer
@ServerHelpers.session_provider
def register_metric_snapshot(session: Session):
    
    # TO-DO: Security
    # signed_timestamp = data['signed_timestamp']
    # public_key = session.query(Device).get(id).public_key
    # if not verify_signature(signed_timestamp, public_key):
    #     return jsonify({'error': 'Invalid signature'}), 400
    
    # Testing:
    
    data = request.get_json()

    if ArgumentParser().getArg("dev_or_prod") == "dev" and 'client_timestamp_utc' not in data:
        data['client_timestamp_utc'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
    
    metric_snapshot = MetricSnapshot(metric_type_id=data['metric_type_id'], value=data['value'], client_timestamp_utc=data['client_timestamp_utc'], client_timezone_mins=data['client_timezone_mins'], server_timestamp_utc=datetime.now(timezone.utc))
    session.add(metric_snapshot)
    session.flush()
    
    
    socketio.emit('data', {"timestamp": str(int(datetime.strptime(metric_snapshot.client_timestamp_utc, '%Y-%m-%dT%H:%M:%S').timestamp() * 1000)), "value": data['value']}, to=str(metric_snapshot.metric_type_id))
    
    return jsonify({'message': 'Metric snapshot posted!', 'id': metric_snapshot.id}), 201
