from sqlalchemy import Column, BigInteger, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

from src.database.entities.base import Base


class Traffic(Base):
    __tablename__ = "traffic"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    direction = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    uf = Column(BigInteger, nullable=False)
    highway = Column(BigInteger, nullable=False)
    km = Column(BigInteger, nullable=False)
    total = Column(BigInteger, nullable=False)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=True)

    route = relationship("Routes", back_populates="traffic")
