from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from base import Base

class PoliceOccurrence(Base):
    __tablename__ = "police_occurrences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    police_occurrence_type_id = Column(BigInteger, ForeignKey("police_occurrence_types.id"), nullable=False)
    description = Column(String(255), nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    occurred_at = Column(Date, nullable=False)
    h3_id = Column(String(20), ForeignKey("hexagons.id"), nullable=False)

    type = relationship("PoliceOccurrenceType", back_populates="occurrences")
    hexagon = relationship("Hexagon", back_populates="police_occurrences")
