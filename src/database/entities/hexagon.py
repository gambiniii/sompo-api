from sqlalchemy import Column, String, Float, BigInteger
from sqlalchemy.orm import relationship

from base import Base

class Hexagon(Base):
    __tablename__ = "hexagons"

    id = Column(String(20), primary_key=True)
    resolution = Column(BigInteger, nullable=False)
    danger_percentage = Column(Float, nullable=False)

    police_occurrences = relationship("PoliceOccurrence", back_populates="hexagon")
    traffic_occurrences = relationship("TrafficOccurrence", back_populates="hexagon")
    stats = relationship("HexagonOccurrenceStats", back_populates="hexagon")
