from flask import Flask, request, jsonify
from sqlalchemy.orm import Session
from src.modules.DatabaseModel.database_model import *
from datetime import datetime, timezone

from src.modules.ServerHelpers.server_helpers import ServerHelpers
from src.modules.Logger.logger import LogLevel, Logger
import time

App = Flask(__name__)

@App.errorhandler(404)
def not_found(error):
    Logger(f"Route not found: {request.url}", LogLevel.WARNING)
    return jsonify({'error': 'Route not found'}), 404


@App.get("/devices")
@ServerHelpers.session_provider
def get_devices(session: Session):
    aggregator_id = request.args.get('aggregator_id')
    if aggregator_id:
        devices = session.query(Device).filter(Device.aggregator_id == aggregator_id).all()
        return jsonify([device.to_dict() for device in devices])    
    devices = session.query(Device).all()
    return jsonify([device.to_dict() for device in devices])

@App.get("/device/<device_id>")
@ServerHelpers.session_provider
def get_device(session: Session, device_id):
    device = session.query(Device).get(device_id)
    return jsonify(device.to_dict())

@App.get("/metric_snapshots/<>")
@ServerHelpers.session_provider
def get_device(session: Session, device_id):
    device = session.query(Device).get(device_id)
    return jsonify(device.to_dict())

@App.get("/aggregators")
@ServerHelpers.session_provider
def get_aggregators(session: Session):
    aggregators = session.query(Aggregator).all()
    return jsonify([aggregator.to_dict() for aggregator in aggregators])

@App.get("/metric_types")
@ServerHelpers.session_provider
def get_metric_types(session: Session):
    metric_types = session.query(MetricType).all()
    return jsonify([metric_type.to_dict() for metric_type in metric_types])

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
    return jsonify({'message': f'Aggregator "{aggregator.name}" registered!', 'id': aggregator.id}), 201


@App.post("/register/device")
@ServerHelpers.timer
@ServerHelpers.session_provider
def register_device(session: Session):
    data = request.get_json()
    device = Device(aggregator_id=data['aggregator_id'], name=data['name'], mac_address=data['mac_address'])
    session.add(device)
    session.flush()
    return jsonify({'message': f'Device "{device.name}" registered!', 'id': device.id}), 201


@App.post("/register/metric_type")
@ServerHelpers.timer
@ServerHelpers.session_provider
def register_metric_type(session: Session):
    data = request.get_json()
    metric_type = MetricType(device_id=data['id'], name=data['name'])
    session.add(metric_type)
    session.flush()
    return jsonify({'message': f'Metric type "{metric_type.name}" registered!', 'id': metric_type.id}), 201


@App.post("/post/metric_snapshot/<id>")
@ServerHelpers.timer
@ServerHelpers.session_provider
def register_metric_snapshot(session: Session, id):
    
    # TO-DO: Security
    # signed_timestamp = data['signed_timestamp']
    # public_key = session.query(Device).get(id).public_key
    # if not verify_signature(signed_timestamp, public_key):
    #     return jsonify({'error': 'Invalid signature'}), 400
    
    data = request.get_json()
    metric_snapshot = MetricSnapshot(metric_type_id=data['metric_type_id'], value=data['value'], client_timestamp_utc=data['client_timestamp_utc'], client_timezone_mins=data['client_timezone_mins'], server_timestamp_utc=datetime.now(timezone.utc))
    session.add(metric_snapshot)
    session.flush()
    return jsonify({'message': 'Metric snapshot posted!', 'id': metric_snapshot.id}), 201
