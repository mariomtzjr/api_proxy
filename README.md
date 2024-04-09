# Proxy de APIs con Traefik and FastApi
Este proyecto es un proxy de APIs desarrollado con FastAPI que utiliza Traefik como reverse proxy

![API Proxy](./documents/api.png)

## Requisitos previos
Antes de comenzar, el sistema o ambiente virtual deberá tener instalado lo siguiente:

- Python 3.x
- Docker
- Nginx
- Mysql
- Traefik
- Redis

## Instalación y configuración
1. Clonar el repositorio:  
   `git clone https://github.com/mariomtzjr/api_proxy.git`  
   `cd api_proxy`  
2. Instalación de dependencias:  
   `pip install -r requirements.txt`
3. Crear red de Docker:  
   `docker network create traefik-public`
4. Configuración de credenciales:  
   `export USERNAME=admin`  
   `export PASSWORD=changeme`  
   `export HASHED_PASSWORD=$(openssl passwd -apr1 $PASSWORD)` De esta manera, el password se almacena como HASH
5. Levantar docker:  
   `docker-compose build`  
   `docker-compose up` # Para ver logs y proceso de despliegue  
   `docker-compose up -d` # Para no obtener salida al levantar el contenedor 
6. Inicialización de  FastAPI (opcional, inicia con docker):
   `uvicorn proxy:app --host 0.0.0.0 --port 8000`
7. Inicialización de Traefik:  
   `docker-compose -f docker-compose-traefik.yml up`

## Run Tests
`pytest -v test/api/test_proxy.py`

### Root path
Open a browser window and go to:  
`localhost:8000/`

### Traefik panel
Open a browser window and go to:  
`localhost:8080` o `traefik.localhost`

### Panelar panel
Open a browser window and go to:  
`panel.localhost:8000/paneler`  
