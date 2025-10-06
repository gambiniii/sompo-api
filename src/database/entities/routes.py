from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from src.database.entities.base import Base


class Routes(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    route = Column(String(255), nullable=False)
    highway = Column(String(255), nullable=False)
    total_traffic = Column(BigInteger, nullable=False)

    # Relacionamento com Traffic
    traffic = relationship("Traffic", back_populates="route")
