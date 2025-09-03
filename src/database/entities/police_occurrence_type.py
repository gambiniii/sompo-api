from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.entities.base import Base


class PoliceOccurrenceType(Base):
    __tablename__ = "police_occurrence_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)

    occurrences = relationship("PoliceOccurrence", back_populates="type")
