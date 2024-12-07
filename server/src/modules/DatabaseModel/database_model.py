from sqlalchemy import Column, Integer, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Aggregator(Base):
    __tablename__ = 'aggregators'

    id = Column(Integer, primary_key=True, autoincrement=True)
    mac_address = Column(Text, nullable=False, unique=True)
    name = Column(Text, nullable=False)

    # Relationship
    devices = relationship("Device", back_populates="aggregator")
    
    def to_dict(self):
        return {
            'id': self.id,
            'mac_address': self.mac_address,
            'name': self.name,
        }

class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    aggregator_id = Column(Integer, ForeignKey('aggregators.id'), nullable=False)
    mac_address = Column(Text, nullable=False, unique=True)
    name = Column(Text, nullable=False)

    # Relationships
    aggregator = relationship("Aggregator", back_populates="devices")
    metric_types = relationship("MetricType", back_populates="device")
    metric_snapshots = relationship("MetricSnapshot", back_populates="device")
    
    def to_dict(self):
        return {
            'id': self.id,
            'aggregator_id': self.aggregator_id,
            'mac_address': self.mac_address,
            'name': self.name,
        }

class MetricType(Base):
    __tablename__ = 'metric_types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey('devices.id'), nullable=False)
    name = Column(Text, nullable=False)

    # Relationships
    device = relationship("Device", back_populates="metric_types")
    metric_values = relationship("MetricValue", back_populates="metric_type")
    
    def to_dict(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'name': self.name
        }

class MetricSnapshot(Base):
    __tablename__ = 'metric_snapshots'

    id = Column(Integer, primary_key=True, autoincrement=True)
    metric_type_id = Column(Integer, ForeignKey('metric_types.id'), nullable=False)
    value = Column(Numeric, nullable=False)
    client_timestamp_utc = Column(Integer, nullable=False)
    client_timezone_mins = Column(Integer, nullable=False)
    server_timestamp_utc = Column(Integer, nullable=False)

    # Relationships
    metric_types = relationship("MetricType", back_populates="metric_snapshots")
    
    def to_dict(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'client_timestamp_utc': self.client_timestamp_utc,
            'client_timezone_mins': self.client_timezone_mins,
            'server_timestamp_utc': self.server_timestamp_utc
        }

# class MetricValue(Base):
#     __tablename__ = 'metric_values'

#     metric_snapshot_id = Column(Integer, ForeignKey('metric_snapshots.id'), primary_key=True)
#     metric_type_id = Column(Integer, ForeignKey('metric_types.id'), primary_key=True)
#     value = Column(Numeric, nullable=False)

#     # Relationships
#     metric_snapshot = relationship("MetricSnapshot", back_populates="metric_values")
#     metric_type = relationship("MetricType", back_populates="metric_values")


