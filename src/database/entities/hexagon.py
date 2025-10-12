from sqlalchemy import Column, String, Float, BigInteger
from sqlalchemy.orm import relationship

from src.database.entities.base import Base


class Hexagon(Base):
    __tablename__ = "hexagons"

    id = Column(String(20), primary_key=True)
    resolution = Column(BigInteger, nullable=False)
    danger_percentage = Column(Float, nullable=False)

    # Relacionamentos removidos: PoliceOccurrence e TrafficOccurrence não existem mais
    stats = relationship("HexagonOccurrenceStats", back_populates="hexagon")
