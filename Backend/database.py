from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# Dados de conexão com o banco
DB_HOST = "localhost"
DB_PORT = "3306"
DB_USER = "root"
DB_PASSWORD = "mysql2026"
DB_NAME = "sistema_cadastro"


DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# Cria a conexão com o banco
engine = create_engine(
    DATABASE_URL,
    echo=False
)


# Cria as sessões do banco
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Base dos modelos
Base = declarative_base()


# Cria uma sessão para acessar o banco
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

