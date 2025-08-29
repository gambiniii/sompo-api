from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database.entities.base import Base


class TrafficOccurrenceType(Base):
    __tablename__ = "traffic_occurrence_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)

    occurrences = relationship("TrafficOccurrence", back_populates="type")