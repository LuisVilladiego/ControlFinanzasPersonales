# 🚀 Guía de Despliegue

Esta guía detallada explica cómo desplegar la aplicación FINANZAS MALU en diferentes entornos.

## 📋 Tabla de Contenidos

1. [Despliegue Local](#despliegue-local)
2. [Despliegue en Producción con Gunicorn](#despliegue-en-producción-con-gunicorn)
3. [Despliegue con Docker](#despliegue-con-docker)
4. [Despliegue en Heroku](#despliegue-en-heroku)
5. [Despliegue en VPS](#despliegue-en-vps)
6. [Configuración de Nginx](#configuración-de-nginx)
7. [Configuración de SSL](#configuración-de-ssl)

---

## 🏠 Despliegue Local

### Desarrollo

```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Ejecutar aplicación
python app.py
```

La aplicación estará en: `http://localhost:5000`

---

## 🏭 Despliegue en Producción con Gunicorn

### Instalación

```bash
pip install gunicorn
```

### Configuración

1. **Crear archivo `gunicorn_config.py`:**

```python
# gunicorn_config.py
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 50
```

2. **Ejecutar con Gunicorn:**

```bash
gunicorn -c gunicorn_config.py app:app
```

### Con systemd (Linux)

1. **Crear servicio `/etc/systemd/system/finanzas.service`:**

```ini
[Unit]
Description=FINANZAS MALU Gunicorn
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/finanzas
Environment="PATH=/var/www/finanzas/venv/bin"
ExecStart=/var/www/finanzas/venv/bin/gunicorn -c gunicorn_config.py app:app

[Install]
WantedBy=multi-user.target
```

2. **Habilitar y iniciar:**

```bash
sudo systemctl daemon-reload
sudo systemctl enable finanzas
sudo systemctl start finanzas
sudo systemctl status finanzas
```

---

## 🐳 Despliegue con Docker

### Dockerfile

```dockerfile
FROM python:3.10-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copiar código
COPY . .

# Exponer puerto
EXPOSE 5000

# Comando por defecto
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=sqlite:///finanzas.db
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  # Opcional: PostgreSQL
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=finanzas
      - POSTGRES_USER=finanzas
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

### Comandos Docker

```bash
# Construir imagen
docker build -t finanzas-app .

# Ejecutar contenedor
docker run -d -p 5000:5000 --name finanzas finanzas-app

# Con docker-compose
docker-compose up -d
docker-compose logs -f
docker-compose down
```

---

## ☁️ Despliegue en Heroku

### Requisitos

1. Cuenta en Heroku
2. Heroku CLI instalado

### Pasos

1. **Login en Heroku:**
```bash
heroku login
```

2. **Crear aplicación:**
```bash
heroku create tu-app-finanzas
```

3. **Configurar variables de entorno:**
```bash
heroku config:set SECRET_KEY=tu-clave-secreta
heroku config:set FLASK_ENV=production
heroku config:set DATABASE_URL=postgresql://...  # Heroku proporciona esto
```

4. **Crear Procfile:**
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT app:app
```

5. **Desplegar:**
```bash
git push heroku main
```

6. **Inicializar base de datos:**
```bash
heroku run python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

7. **Abrir aplicación:**
```bash
heroku open
```

### Add-ons Recomendados

```bash
# PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Scheduler (para recordatorios)
heroku addons:create scheduler:standard
```

---

## 🖥️ Despliegue en VPS

### Requisitos del Servidor

- Ubuntu 20.04+ o Debian 11+
- 1GB RAM mínimo
- 10GB almacenamiento
- Acceso root o sudo

### Instalación Completa

#### 1. Actualizar Sistema

```bash
sudo apt update
sudo apt upgrade -y
```

#### 2. Instalar Dependencias

```bash
sudo apt install -y python3-pip python3-venv nginx git
```

#### 3. Clonar Repositorio

```bash
cd /var/www
sudo git clone https://github.com/tu-usuario/Finanzas.git
sudo chown -R $USER:$USER Finanzas
cd Finanzas
```

#### 4. Configurar Entorno Virtual

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

#### 5. Configurar Variables de Entorno

```bash
cp .env.example .env
nano .env  # Editar con tus valores
```

#### 6. Inicializar Base de Datos

```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

#### 7. Probar con Gunicorn

```bash
gunicorn -w 4 -b 127.0.0.1:5000 app:app
```

#### 8. Configurar systemd (ver sección anterior)

#### 9. Configurar Nginx (ver sección siguiente)

---

## 🌐 Configuración de Nginx

### Archivo de Configuración

Crear `/etc/nginx/sites-available/finanzas`:

```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/finanzas/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

### Habilitar Sitio

```bash
sudo ln -s /etc/nginx/sites-available/finanzas /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 🔒 Configuración de SSL

### Con Let's Encrypt (Certbot)

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com

# Renovación automática
sudo certbot renew --dry-run
```

### Configuración Nginx con SSL

```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tu-dominio.com www.tu-dominio.com;

    ssl_certificate /etc/letsencrypt/live/tu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tu-dominio.com/privkey.pem;

    # Configuración SSL recomendada
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 📊 Monitoreo y Logs

### Ver Logs de Gunicorn

```bash
# Si usas systemd
sudo journalctl -u finanzas -f

# Logs de Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Configurar Logging en la Aplicación

Agregar en `config.py`:

```python
import logging
from logging.handlers import RotatingFileHandler

# Configurar logging
if not app.debug:
    file_handler = RotatingFileHandler('logs/finanzas.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Finanzas startup')
```

---

## 🔄 Actualizaciones

### Proceso de Actualización

```bash
# 1. Hacer backup de la base de datos
cp finanzas.db finanzas.db.backup

# 2. Detener servicio
sudo systemctl stop finanzas

# 3. Actualizar código
git pull origin main

# 4. Actualizar dependencias
source venv/bin/activate
pip install -r requirements.txt

# 5. Ejecutar migraciones (si hay)
flask db upgrade

# 6. Reiniciar servicio
sudo systemctl start finanzas
```

---

## ✅ Checklist de Despliegue

- [ ] Servidor configurado
- [ ] Python 3.9+ instalado
- [ ] Entorno virtual creado
- [ ] Dependencias instaladas
- [ ] Variables de entorno configuradas
- [ ] Base de datos inicializada
- [ ] Gunicorn configurado
- [ ] Systemd service creado
- [ ] Nginx configurado
- [ ] SSL configurado
- [ ] Firewall configurado
- [ ] Backups configurados
- [ ] Monitoreo configurado

---

## 🆘 Troubleshooting

### Error: "Address already in use"

```bash
# Encontrar proceso usando el puerto
sudo lsof -i :5000
# Matar proceso
sudo kill -9 <PID>
```

### Error: "Permission denied"

```bash
# Dar permisos correctos
sudo chown -R www-data:www-data /var/www/finanzas
sudo chmod -R 755 /var/www/finanzas
```

### La aplicación no responde

1. Verificar que Gunicorn está corriendo: `sudo systemctl status finanzas`
2. Verificar logs: `sudo journalctl -u finanzas -n 50`
3. Verificar Nginx: `sudo nginx -t`
4. Verificar firewall: `sudo ufw status`

---

**¡Despliegue exitoso!** 🎉

