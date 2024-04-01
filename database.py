from datetime import datetime
import json
import os
import time

import pymysql
import redis

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
redis_client = redis.Redis(
    host=os.environ.get('REDIS_HOST'),
    port=int(os.environ.get('REDIS_PORT')),
    decode_responses=True,
    db=0
)

# Crear la base de datos si no existe
Base.metadata.create_all(bind=engine)

# Crear una sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Funciones para interactuar con la base de datos
def log_request(ip: str, path: str):
    print("***** database.log_request *****")
    db = SessionLocal()
    db.add(UsageStat(ip=ip, path=path))
    db.commit()
    db.close()

def get_stats():
    print("***** database.get_stats *****")
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
    print("***** database.get_request_count_by_ip *****")
    db = SessionLocal()
    count = db.query(UsageStat).filter(UsageStat.ip == ip).count()
    db.close()
    return count

def get_request_count_by_path(path: str):
    print("***** database.get_request_count_by_path *****")
    db = SessionLocal()
    count = db.query(UsageStat).filter(UsageStat.path == path).count()
    db.close()
    return count

def check_database_connection():
    print("***** database.check_database_connection *****")
    attempts = 0
    while attempts < 3:
        try:
            conn = pymysql.connect(
                host=DB_HOST,
                user=DB_USERNAME,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            return conn
        except pymysql.Error as e:
            print(f"Error connecting to database: {e}")
            attempts += 1
            time.sleep(3)  # Esperar antes de volver a intentar la conexión
    raise Exception("Failed to connect to database after multiple attempts")

# Función para almacenar datos en Redis
def store_data_in_redis(key, value):
    print("***** database.store_data_in_redis *****")
    redis_client.set(key, value)

# Función para recuperar datos de Redis
def get_data_from_redis(key):
    print("***** database.get_data_from_redis *****")
    try:
        formatted_response = json.loads(redis_client.get(key))
        return formatted_response
    except json.JSONDecodeError as error:
        print("Error getting data from redis: ", error)
    return {}
