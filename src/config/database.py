from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus  # Import para codificar a senha

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()


# Constrói a URL de conexão
password = os.getenv("POSTGRES_PASS")
encoded_password = quote_plus(password)  # Isso converterá @ para %40

# Constrói a URL de conexão com a senha codificada
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{encoded_password}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB_NAME')}"

# Cria o engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    echo=False,
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
