from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

# Crear una instancia de la clase base declarativa
Base = declarative_base()

# Modelo de datos para la tabla de estadísticas
class UsageStat(Base):
    __tablename__ = 'usage_stats'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(255))
    path = Column(String(255))
    timestamp = Column(DateTime, default=datetime.now)