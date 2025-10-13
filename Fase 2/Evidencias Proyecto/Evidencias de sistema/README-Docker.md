# Calendario Judicial - Docker

Este proyecto incluye configuración completa de Docker para desarrollo y producción.

## 🐳 Archivos Docker

- `Dockerfile` - Imagen base de la aplicación
- `docker-compose.yml` - Configuración de producción (PostgreSQL + Nginx + Gunicorn)
- `docker-compose.dev.yml` - Configuración de desarrollo (solo PostgreSQL + Django dev server)
- `nginx.conf` - Configuración de Nginx para producción
- `.dockerignore` - Archivos a ignorar en la imagen Docker

## 🚀 Uso Rápido

### Desarrollo
```bash
# Iniciar solo la base de datos
docker-compose -f docker-compose.dev.yml up db

# O iniciar todo el entorno de desarrollo
docker-compose -f docker-compose.dev.yml up
```

### Producción
```bash
# Construir y ejecutar todo
docker-compose up --build

# En segundo plano
docker-compose up -d
```

## 📋 Comandos Útiles

### Desarrollo
```bash
# Crear superusuario
docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser --settings=calendario_judicial.settings_dev

# Ejecutar migraciones
docker-compose -f docker-compose.dev.yml exec web python manage.py migrate --settings=calendario_judicial.settings_dev

# Cargar datos de prueba
docker-compose -f docker-compose.dev.yml exec web python manage.py loaddata plazos/fixtures/codigos_procedimiento.json --settings=calendario_judicial.settings_dev

# Acceder al shell de Django
docker-compose -f docker-compose.dev.yml exec web python manage.py shell --settings=calendario_judicial.settings_dev
```

### Producción
```bash
# Crear superusuario
docker-compose exec web python manage.py createsuperuser

# Ejecutar migraciones
docker-compose exec web python manage.py migrate

# Recopilar archivos estáticos
docker-compose exec web python manage.py collectstatic --noinput

# Ver logs
docker-compose logs -f web
```

## 🔧 Configuración

### Variables de Entorno

#### Desarrollo
- `DEBUG=True`
- `DATABASE_URL=postgresql://postgres:postgres123@db:5432/calendario_judicial_dev`
- `SECRET_KEY=clave-desarrollo-no-segura`

#### Producción
- `DEBUG=False`
- `DATABASE_URL=postgresql://postgres:postgres123@db:5432/calendario_judicial`
- `SECRET_KEY=tu-clave-secreta-muy-segura-aqui`

### Puertos
- **8000**: Aplicación Django (desarrollo)
- **80**: Nginx (producción)
- **5432**: PostgreSQL

## 📁 Volúmenes

- `postgres_data`: Datos de PostgreSQL (producción)
- `postgres_data_dev`: Datos de PostgreSQL (desarrollo)
- `static_volume`: Archivos estáticos
- `media_volume`: Archivos de medios

## 🛠️ Personalización

### Cambiar contraseña de PostgreSQL
Edita `docker-compose.yml` y `docker-compose.dev.yml`:
```yaml
environment:
  POSTGRES_PASSWORD: tu-nueva-contraseña
```

### Cambiar puerto de la aplicación
Edita `docker-compose.yml`:
```yaml
ports:
  - "8080:8000"  # Cambiar 8080 por el puerto deseado
```

## 🔍 Troubleshooting

### Limpiar contenedores y volúmenes
```bash
# Detener y eliminar contenedores
docker-compose down

# Eliminar volúmenes (¡CUIDADO! Esto borra la base de datos)
docker-compose down -v

# Reconstruir desde cero
docker-compose up --build --force-recreate
```

### Ver logs de errores
```bash
# Logs de la aplicación
docker-compose logs web

# Logs de la base de datos
docker-compose logs db

# Logs de Nginx
docker-compose logs nginx
```

### Acceder a la base de datos
```bash
# Conectar a PostgreSQL
docker-compose exec db psql -U postgres -d calendario_judicial
```

## 📝 Notas

- El proyecto se ejecuta en `/app` dentro del contenedor
- Los archivos estáticos se sirven a través de Nginx en producción
- La base de datos PostgreSQL persiste entre reinicios
- Para desarrollo, se recomienda usar `docker-compose.dev.yml`
- Para producción, usar `docker-compose.yml` con Nginx
