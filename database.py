from datetime import datetime
import os

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Crear una instancia de la clase base declarativa
Base = declarative_base()

# Definir el modelo de datos para la tabla de estadísticas
class UsageStat(Base):
    __tablename__ = 'usage_stats'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(255))
    path = Column(String(255))
    timestamp = Column(DateTime, default=datetime.now)

# Configurar la conexión a la base de datos
DB_HOST = os.environ.get('DB_HOST', '')
DB_USERNAME = os.environ.get('DB_USERNAME', '')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
DB_NAME = os.environ.get('DB_NAME', '')
DB_PORT = os.environ.get('DB_PORT', '')

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

# Crear la base de datos si no existe
Base.metadata.create_all(bind=engine)

# Crear una sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Funciones para interactuar con la base de datos
def log_request(ip: str, path: str):
    db = SessionLocal()
    db.add(UsageStat(ip=ip, path=path))
    db.commit()
    db.close()

def get_stats():
    db = SessionLocal()
    stats = db.query(UsageStat).all()
    db.close()
    return [{"ip": stat.ip, "path": stat.path, "timestamp": stat.timestamp} for stat in stats]

def get_limit(ip: str):
    db = SessionLocal()
    count = db.query(UsageStat).filter(UsageStat.ip == ip).count()
    db.close()
    return {"ip": ip, "limit": count}

def get_request_count_by_ip(ip: str):
    db = SessionLocal()
    count = db.query(UsageStat).filter(UsageStat.ip == ip).count()
    db.close()
    return count

def get_request_count_by_path(path: str):
    db = SessionLocal()
    count = db.query(UsageStat).filter(UsageStat.path == path).count()
    db.close()
    return count