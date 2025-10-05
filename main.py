from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes.risk_routes import risk_router
from src.api.routes.database_routes import database_router
from src.api.routes.police_occurrence_routes import police_occurrence_router
from src.api.routes.traffic_occurrence_routes import traffic_occurrence_router

from src.database.entities.init import __all__
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:5173",  # Vite
        "http://localhost:8080",  # Vue CLI
        "http://localhost:4200",  # Angular
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
app.include_router(database_router)
app.include_router(police_occurrence_router)
app.include_router(traffic_occurrence_router)
