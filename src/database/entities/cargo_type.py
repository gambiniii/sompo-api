from sqlalchemy import Column, BigInteger, String, Float, Text

from src.database.entities.base import Base


class CargoType(Base):
    __tablename__ = "cargo_type"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    categoria = Column(String(50), nullable=False)
    risco_roubo_percentual = Column(Float, nullable=False)
    risco_acidente_percentual = Column(Float, nullable=False)
    descricao = Column(String(500), nullable=False)
    exemplos = Column(Text, nullable=True)
    riscos_principais = Column(String(500), nullable=True)
    impacto_ambiental = Column(String(100), nullable=True)
