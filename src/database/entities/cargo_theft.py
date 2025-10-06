from sqlalchemy import Column, Integer, String, Float, Date

from src.database.entities.base import Base


class CargoTheft(Base):
    __tablename__ = "cargo_theft"

    id = Column(Integer, primary_key=True, autoincrement=True)
    state = Column(String(2), nullable=False)
    city = Column(String(255), nullable=False)
    neighborhood = Column(String(255), nullable=False)
    street = Column(String(255), nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    occurred_at = Column(Date, nullable=False)
