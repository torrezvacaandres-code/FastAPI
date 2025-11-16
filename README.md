# FastAPI Hexagonal Architecture Skeleton

Proyecto base FastAPI con arquitectura hexagonal, listo para comenzar a desarrollar. Solo necesitas configurar las credenciales de base de datos y empezar a programar.

## 🏗️ Arquitectura

Este proyecto sigue una **Arquitectura Hexagonal** (también conocida como Arquitectura de Puertos y Adaptadores), que separa la lógica de negocio de los detalles de infraestructura.

```
app/
  core/           # Configuración y utilidades cross-cutting
  domain/         # Lógica de negocio pura (entidades, value objects, excepciones)
  usecases/       # Casos de uso que orquestan la lógica de negocio
  adapters/       # Adaptadores de infraestructura (HTTP, DB, etc.)
    http/         # Routers y controladores FastAPI
    db/           # Modelos ORM y repositorios
```

Para más detalles, consulta [ARCHITECTURE.md](./ARCHITECTURE.md).

## 🚀 Inicio Rápido

### Prerrequisitos

- Docker y Docker Compose instalados
- Python 3.12+ (si quieres ejecutar localmente sin Docker)

### Configuración

1. **Clona el repositorio** (si aún no lo has hecho)

2. **Crea el archivo `.env`** basándote en `.env.example`:
   ```bash
   cp .env.example .env
   ```

3. **Edita `.env`** y configura tus credenciales de base de datos:
   ```env
   APP_DB_USER=tu_usuario
   APP_DB_PASSWORD=tu_contraseña
   APP_DB_NAME=tu_base_de_datos
   ```

4. **Inicia los servicios con Docker Compose**:
   ```bash
   docker compose up -d
   ```

5. **Aplica las migraciones** (si es necesario):
   ```bash
   docker compose run --rm api alembic upgrade head
   ```

6. **Verifica que todo funciona**:
   - Health check: http://localhost:8000/health
   - Database check: http://localhost:8000/db-check
   - Documentación API: http://localhost:8000/docs

## 📝 Variables de Entorno

El proyecto usa variables de entorno con el prefijo `APP_`. Las principales son:

| Variable | Descripción | Default |
|----------|-------------|---------|
| `APP_APP_NAME` | Nombre de la aplicación | FastAPI Hexagonal Skeleton |
| `APP_ENVIRONMENT` | Entorno (development/production) | development |
| `APP_DB_USER` | Usuario de PostgreSQL | postgres |
| `APP_DB_PASSWORD` | Contraseña de PostgreSQL | postgres |
| `APP_DB_HOST` | Host de PostgreSQL | db |
| `APP_DB_PORT` | Puerto de PostgreSQL | 5432 |
| `APP_DB_NAME` | Nombre de la base de datos | app_db |
| `APP_DATABASE_URL` | URL completa de conexión (alternativa) | - |
| `APP_CORS_ORIGINS` | Orígenes permitidos para CORS | ["http://localhost:3000", "http://localhost:8000"] |
| `APP_LOG_LEVEL` | Nivel de logging | INFO |

## 🗄️ Base de Datos y Migraciones

### Crear una nueva migración

```bash
docker compose run --rm api alembic revision --autogenerate -m "descripción del cambio"
```

### Aplicar migraciones

```bash
docker compose run --rm api alembic upgrade head
```

### Revertir última migración

```bash
docker compose run --rm api alembic downgrade -1
```

### Ver historial de migraciones

```bash
docker compose run --rm api alembic history
```

## 🏃 Desarrollo Local (sin Docker)

Si prefieres ejecutar el proyecto localmente:

1. **Crea un entorno virtual**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   ```

2. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configura la base de datos**:
   - Asegúrate de tener PostgreSQL corriendo
   - Actualiza las variables `APP_DB_*` en tu `.env`

4. **Ejecuta la aplicación**:
   ```bash
   uvicorn app.main:app --reload
   ```

## 📁 Estructura del Proyecto

```
.
├── alembic/              # Migraciones de base de datos
│   ├── versions/         # Versiones de migraciones
│   └── env.py           # Configuración de Alembic
├── alembic.ini          # Configuración de Alembic
├── app/
│   ├── adapters/        # Adaptadores de infraestructura
│   │   ├── db/          # Modelos ORM y repositorios
│   │   └── http/        # Routers y controladores FastAPI
│   ├── core/            # Configuración y utilidades
│   │   ├── config.py    # Configuración de la aplicación
│   │   ├── database.py  # Configuración de SQLAlchemy
│   │   ├── logging.py   # Configuración de logging
│   │   └── middleware.py # Middlewares personalizados
│   ├── domain/          # Lógica de negocio
│   │   ├── entities/    # Entidades de dominio
│   │   ├── value_objects/ # Objetos valor
│   │   └── exceptions.py # Excepciones del dominio
│   ├── usecases/        # Casos de uso
│   └── main.py          # Punto de entrada
├── docker-compose.yml   # Configuración de Docker Compose
├── Dockerfile           # Imagen Docker de la aplicación
├── requirements.txt     # Dependencias Python
├── .env.example         # Template de variables de entorno
├── .gitignore           # Archivos ignorados por Git
└── README.md           # Este archivo
```

## 🔧 Comandos Útiles

### Docker Compose

```bash
# Iniciar servicios
docker compose up -d

# Ver logs
docker compose logs -f api

# Detener servicios
docker compose down

# Reconstruir imagen
docker compose build --no-cache api
```

### Desarrollo

```bash
# Ver logs en tiempo real
docker compose logs -f api

# Ejecutar comandos dentro del contenedor
docker compose exec api bash

# Reiniciar solo el servicio de API
docker compose restart api
```

## 🎯 Próximos Pasos

1. **Define tus entidades de dominio** en `app/domain/entities/`
2. **Crea tus modelos ORM** en `app/adapters/db/`
3. **Implementa repositorios** en `app/adapters/db/repositories/`
4. **Define casos de uso** en `app/usecases/`
5. **Crea tus endpoints** en `app/adapters/http/`

## 📚 Recursos

- [Documentación de FastAPI](https://fastapi.tiangolo.com/)
- [Documentación de SQLAlchemy](https://docs.sqlalchemy.org/)
- [Documentación de Alembic](https://alembic.sqlalchemy.org/)
- [Arquitectura Hexagonal](https://alistair.cockburn.us/hexagonal-architecture/)

## 📄 Licencia

Este es un proyecto de código abierto. Siéntete libre de usarlo como base para tus proyectos.

