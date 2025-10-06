from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends

Base = declarative_base()

# Configuração do SQLAlchemy para FastAPI
engine = None
SessionLocal = None

def get_db() -> Session:
    """Dependency para obter a sessão de banco de dados"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def setup_db(db_url: str):
    """Configura a conexão com o banco de dados"""
    global engine, SessionLocal
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    return {'engine': engine, 'session': SessionLocal}