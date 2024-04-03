import json
import os
import time

import pymysql
import redis

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import UsageStat

# Configurar la conexión a la base de datos
DB_HOST = os.environ.get('DB_HOST', '')
DB_USERNAME = os.environ.get('DB_USERNAME', '')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
DB_ROOT_PASSWORD = os.environ.get('DB_ROOT_PASSWORD', '')
DB_NAME = os.environ.get('DB_NAME', '')
DB_PORT = os.environ.get('DB_PORT', '')

DB_URL = f"mysql+pymysql://root:{DB_ROOT_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DB_URL)


class DBManager:

    def __init__(self) -> None:
        
        # Crear una sesión de base de datos
        self.sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        self.redis_client = redis.Redis(
            host=os.environ.get('REDIS_HOST'),
            port=int(os.environ.get('REDIS_PORT')),
            decode_responses=True,
            db=0
        )

    # Funciones para interactuar con la base de datos
    def log_request(self, ip: str, path: str):
        print("***** database.log_request *****")
        db = self.sessionLocal()
        db.add(UsageStat(ip=ip, path=path))
        db.commit()
        db.close()

    def get_stats(self):
        print("***** database.get_stats *****")
        db = self.sessionLocal()
        stats = db.query(UsageStat).all()
        db.close()
        return [{"ip": stat.ip, "path": stat.path, "timestamp": stat.timestamp} for stat in stats]

    def get_limit(self, ip: str):
        db = self.sessionLocal()
        count = db.query(UsageStat).filter(UsageStat.ip == ip).count()
        db.close()
        return {"ip": ip, "limit": count}

    def get_request_count_by_ip(self, ip: str):
        print("***** database.get_request_count_by_ip *****")
        db = self.sessionLocal()
        count = db.query(UsageStat).filter(UsageStat.ip == ip).count()
        db.close()
        return count

    def get_request_count_by_path(self, path: str):
        print("***** database.get_request_count_by_path *****")
        db = self.sessionLocal()
        count = db.query(UsageStat).filter(UsageStat.path == path).count()
        db.close()
        return count

    # Función para almacenar datos en Redis
    def store_data_in_redis(self, key: str, value: str):
        print("***** database.store_data_in_redis *****")
        self.redis_client.set(key, value)

    # Función para recuperar datos de Redis
    def __get_data_from_redis(self, key: str):
        """Protected method example

        Args:
            key (str): name  of key to return the value for given key

        Returns:
            str: stored value for key
        """
        print("***** database.get_data_from_redis *****")
        try:
            formatted_response = json.loads(self.redis_client.get(key))
            return formatted_response
        except json.JSONDecodeError as error:
            print("Error getting data from redis: ", error)
        except TypeError as type_error:
            print(type_error)
        return {}
    
    def get_redis_data(self, key: str):
        return self.__get_data_from_redis(key)
