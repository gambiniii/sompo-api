from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# URL de conexão - pode vir do .env
DATABASE_URL = "postgresql://user:password@localhost:5432/mydb"

# Cria o engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # testa a conexão antes de usar
    echo=False            # se quiser ver os SQLs no log, troca para True
)

# Cria a factory de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependência para usar no FastAPI (injeta sessão)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
