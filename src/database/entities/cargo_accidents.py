from sqlalchemy import Column, BigInteger, Integer, String, Float, Date, Time

from src.database.entities.base import Base


class CargoAccidents(Base):
    __tablename__ = "cargo_accidents"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    state = Column(String(2), nullable=False)
    highway = Column(String(255), nullable=False)
    kilometer = Column(BigInteger, nullable=False)
    city = Column(String(255), nullable=False)
    accident_cause = Column(String(255), nullable=False)
    accident_type = Column(String(255), nullable=False)
    accident_classification = Column(String(255), nullable=False)
    day_period = Column(String(255), nullable=False)
    road_direction = Column(String(255), nullable=False)
    weather_condition = Column(String(255), nullable=False)
    road_type = Column(String(255), nullable=False)
    road_layout = Column(String(255), nullable=False)
    land_use = Column(String(255), nullable=False)
    people = Column(Integer, nullable=False)
    deaths = Column(BigInteger, nullable=False)
    minor_injuries = Column(BigInteger, nullable=False)
    serious_injuries = Column(BigInteger, nullable=False)
    unharmed = Column(BigInteger, nullable=False)
    unknown = Column(BigInteger, nullable=False)
    injured = Column(BigInteger, nullable=False)
    vehicles = Column(BigInteger, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
