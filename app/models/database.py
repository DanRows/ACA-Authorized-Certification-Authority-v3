import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ClientStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    status = Column(Enum(ClientStatus), default=ClientStatus.PENDING)
    satisfaction_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.now)
    last_service = Column(DateTime, nullable=True)

    # Relación con equipos
    equipment = relationship("Equipment", back_populates="client")

class Equipment(Base):
    __tablename__ = 'equipment'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    type = Column(String)
    calibration_date = Column(DateTime, nullable=True)
    next_calibration = Column(DateTime, nullable=True)
    status = Column(String, default='pending')

    # Relación con cliente
    client = relationship("Client", back_populates="equipment")
