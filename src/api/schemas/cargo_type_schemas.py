from pydantic import BaseModel, Field
from typing import Optional


class CargoTypeBase(BaseModel):
    categoria: str = Field(..., min_length=1, max_length=50)
    risco_roubo_percentual: float = Field(..., ge=0)
    risco_acidente_percentual: float = Field(..., ge=0)
    descricao: str = Field(..., min_length=1, max_length=500)
    exemplos: Optional[str] = None
    riscos_principais: Optional[str] = Field(None, max_length=500)
    impacto_ambiental: Optional[str] = Field(None, max_length=100)


class CargoTypeCreate(CargoTypeBase):
    pass


class CargoTypeUpdate(BaseModel):
    categoria: Optional[str] = Field(None, min_length=1, max_length=50)
    risco_roubo_percentual: Optional[float] = Field(None, ge=0)
    risco_acidente_percentual: Optional[float] = Field(None, ge=0)
    descricao: Optional[str] = Field(None, min_length=1, max_length=500)
    exemplos: Optional[str] = None
    riscos_principais: Optional[str] = Field(None, max_length=500)
    impacto_ambiental: Optional[str] = Field(None, max_length=100)


class CargoTypeOut(CargoTypeBase):
    id: int

    class Config:
        from_attributes = True


class CargoTypeParams(BaseModel):
    categoria: Optional[str] = None
    descricao: Optional[str] = None
    min_risco_roubo: Optional[float] = None
    max_risco_roubo: Optional[float] = None
    min_risco_acidente: Optional[float] = None
    max_risco_acidente: Optional[float] = None
    impacto_ambiental: Optional[str] = None
    limit: int = 100
    offset: int = 0
