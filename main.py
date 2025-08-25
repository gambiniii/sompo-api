from fastapi import FastAPI
from src.api.routes.routes import risk_router

app = FastAPI(
    title="Sompo API - Sistema de Avaliação de Riscos",
    description="API para avaliação de riscos em trajetos e gerenciamento de seguros",
    version="1.0.0",
    contact={
        "name": "Equipe Sompo",
        "email": "suporte@sompo.com.br",
    },
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


app.include_router(risk_router)
