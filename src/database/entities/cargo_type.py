from sqlalchemy import Column, BigInteger, String

from src.database.entities.base import Base


class CargoType(Base):
    __tablename__ = "cargo_type"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    theft = Column(BigInteger, nullable=False)
    accident = Column(BigInteger, nullable=False)
    irtc = Column(BigInteger, nullable=False)
    global_risk_level = Column(BigInteger, nullable=False)
