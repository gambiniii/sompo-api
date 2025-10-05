from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.api.logic.cargo_theft import CargoTheftLogic

class CargoTheftController:
    def __init__(self, db: Session):
        self.logic = CargoTheftLogic(db)

    def list(self, **filters):
        try:
            return self.logic.list(**filters)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
