from sqlalchemy import Column, Integer, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Aggregator(Base):
    __tablename__ = 'aggregators'

    id = Column(Integer, primary_key=True, autoincrement=True)
    guid = Column(Text, unique=True, nullable=False)
    name = Column(Text, nullable=False)

    # Relationship
    devices = relationship("Device", back_populates="aggregator")

class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    aggregator_id = Column(Integer, ForeignKey('aggregators.id'), nullable=False)
    name = Column(Text, nullable=False)
    ordinal = Column(Integer, nullable=False)

    # Relationships
    aggregator = relationship("Aggregator", back_populates="devices")
    metric_types = relationship("MetricType", back_populates="device")
    metric_snapshots = relationship("MetricSnapshot", back_populates="device")

class MetricType(Base):
    __tablename__ = 'metric_types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey('devices.id'), nullable=False)
    name = Column(Text, nullable=False)

    # Relationships
    device = relationship("Device", back_populates="metric_types")
    metric_values = relationship("MetricValue", back_populates="metric_type")

class MetricSnapshot(Base):
    __tablename__ = 'metric_snapshots'

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey('devices.id'), nullable=False)
    client_timestamp_utc = Column(Integer, nullable=False)
    client_timezone_mins = Column(Integer, nullable=False)
    server_timestamp_utc = Column(Integer, nullable=False)
    server_timezone_mins = Column(Integer, nullable=False)

    # Relationships
    device = relationship("Device", back_populates="metric_snapshots")
    metric_values = relationship("MetricValue", back_populates="metric_snapshot")

class MetricValue(Base):
    __tablename__ = 'metric_values'

    metric_snapshot_id = Column(Integer, ForeignKey('metric_snapshots.id'), primary_key=True)
    metric_type_id = Column(Integer, ForeignKey('metric_types.id'), primary_key=True)
    value = Column(Numeric, nullable=False)

    # Relationships
    metric_snapshot = relationship("MetricSnapshot", back_populates="metric_values")
    metric_type = relationship("MetricType", back_populates="metric_values")
