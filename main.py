from fastapi import FastAPI
from api.routes.risk_routes import risk_router
from api.routes.police_occurrence_routes import police_occurrence_router
from src.config.database import engine
from src.database.entities.base import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sompo API - Sistema de Avaliação de Riscos",
    description="API para avaliação de riscos em trajetos e gerenciamento de seguros",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "risks",
            "description": "Operações relacionadas à avaliação de riscos em trajetos",
        }
    ],
)

# Health check endpoint
@app.get("/", tags=["Health Check"])
async def root():
    return {
        "message": "Sompo API está funcionando!",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}


# Registra as rotas
app.include_router(risk_router)
app.include_router(police_occurrence_router)