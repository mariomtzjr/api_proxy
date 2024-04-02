# Proxy de APIs con FastAPI, NGINX, Prometheus y Grafana
Este proyecto es un proxy de APIs desarrollado con FastAPI que utiliza NGINX para el control de acceso y límites de tasa, y Prometheus y Grafana para la monitorización y visualización de estadísticas.

## Requisitos previos
Antes de comenzar, el sistema deberá o ambiente virtual deberá tener instalado lo siguiente:

- Python 3.x
- Docker
- Nginx
- Mysql
- Prometheus
- Grafana
- Redis

## Instalación y configuración
1. Clonar el repositorio:  
   `git clone https://github.com/mariomtzjr/api_proxy.git`  
   `cd api_proxy`  
2. Instalación de dependencias:  
   `pip install -r requirements.txt`
3. Levantar docker:  
   `docker-compose build`  
   `docker-compose up` # Para ver logs y proceso de despliegue  
   `docker-compose up -d` # Para no obtener salida al levantar el contenedor 
4. Configuración de NGINX:
   - Copia el archivo nginx.conf a la ubicación de configuración de NGINX.
   - Actualiza la configuración; dirección del servidor y los límites de tasa (esta configuración dependerá de tus necesidades).
5. Configuración de Prometheus:  
   - Copia el archivo prometheus.yml a la ubicación de configuración de Prometheus.
   - Actualiza la configuración según la dirección del servidor de FastAPI.
6. Inicialización de  FastAPI:
   `uvicorn proxy:app --host 0.0.0.0 --port 8000`
7. Inicialización de NGINX:  
   `sudo systemctl start nginx`
8. Inicialización de Prometheus:
   `./prometheus --config.file=prometheus.yml`
9.  Inicialización de Grafana:
   - Accede a la interfaz web de Grafana, usuario por defaualt `admin`, password `admin`
   - Configura un origen de datos Prometheus.
   - Importa un panel predefinido para visualizar las métricas de FastAPI.

### Prometheus panel
Open a browser window and go to:  
`localhost:9090`

### Grafana panel
Open a browser window and go to:  
`localhost:3000`  