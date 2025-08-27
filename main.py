from fastapi import FastAPI
from src.api.routes.routes import risk_router
from src.api.routes.police_occurrence import police_occurrence_router
# from src.config.database import engine
# from src.database.entities.base import Base

# Cria as tabelas no banco (apenas se não estiver usando migrations)
# Base.metadata.create_all(bind=engine)

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
