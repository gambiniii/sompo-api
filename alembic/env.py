from pathlib import Path
import sys, os

# adiciona <repo_root> (pai do alembic) ao sys.path antes de qualquer import de src.*
ROOT = Path(__file__).resolve().parents[1]  # projeto root (onde está alembic.ini)
PROJECT_ROOT = str(ROOT)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

from src.database.entities.base import Base

config = context.config

user = os.getenv("POSTGRES_USER", "postgres")
pwd = os.getenv("POSTGRES_PASS", "")
host = os.getenv("POSTGRES_HOST", "127.0.0.1")
port = os.getenv("POSTGRES_PORT", "5432")
db   = os.getenv("POSTGRES_DB_NAME", "sompo")
db_url = f"postgresql://{user}:{quote_plus(pwd)}@{host}:{port}/{db}"

# duplicar '%' para evitar interpolação do ConfigParser (ex: %40)
db_url_escaped = db_url.replace("%", "%%")
config.set_main_option("sqlalchemy.url", db_url_escaped)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
