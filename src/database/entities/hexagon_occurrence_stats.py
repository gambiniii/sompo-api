from sqlalchemy import Column, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from src.database.entities.base import Base


class HexagonOccurrenceStats(Base):
    __tablename__ = "hexagon_occurrence_stats"

    h3_id = Column(String(20), ForeignKey("hexagons.id"), primary_key=True)
    occurrence_type = Column(String(50), primary_key=True)  # 'police' ou 'traffic'
    type_id = Column(BigInteger, primary_key=True)
    count = Column(BigInteger, nullable=False)

    hexagon = relationship("Hexagon", back_populates="stats")
