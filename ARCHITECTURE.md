# Arquitectura Hexagonal para FastAPI

Este documento describe la estructura del proyecto, responsabilidades por carpeta y cómo trabajar con migraciones (Alembic) y base de datos. El objetivo es mantener un diseño portátil, testeable y desacoplado.

## Visión general
- Núcleo de negocio aislado en `app/domain` y coordinado por `app/usecases`.
- FastAPI y la infraestructura viven en `app/adapters`.
- Configuración y utilidades cross-cutting en `app/core`.
- Migraciones con Alembic en `alembic/`.

```
app/
  core/
    config.py
    database.py
  domain/
    entities/
    value_objects/
    exceptions.py
  usecases/
  adapters/
    http/
      api.py
    db/
      repositories/
main.py
alembic/
  env.py
  versions/
Dockerfile
requirements.txt
docker-compose.yml
```

## Capas y responsabilidades

### 1) app/domain (Dominio)
- Entidades y reglas del negocio puras.
- Sin dependencias en frameworks ni en infraestructura.
- Define puertos (interfaces) que la infraestructura debe implementar (por ejemplo, `UserRepository`).
- Carpetas:
  - `entities/`: clases de entidad (p. ej., `User`, `Order`).
  - `value_objects/`: objetos valor inmutables (p. ej., `Email`, `Money`).
  - `exceptions.py`: errores del dominio.

### 2) app/usecases (Aplicación)
- Orquesta casos de uso y coordina repositorios a través de los puertos del dominio.
- No contiene detalles de HTTP, DB ni frameworks.
- Expone métodos/servicios que usan controladores del borde (HTTP, tareas background, etc.).

### 3) app/adapters (Bordes / Infraestructura)
- Conecta el mundo externo con los puertos del dominio.
- Subcarpetas comunes:
  - `http/`: routers y controladores FastAPI. Validación de request/response (Pydantic), dependencias, errores HTTP.
  - `db/`: modelos ORM (SQLAlchemy), mappers y repositorios que implementan las interfaces del dominio. Aquí viven los detalles de persistencia.
  - `tasks/` (opcional): definición de workers (Celery, RQ) e integración con colas.

### 4) app/core (Cross-cutting)
- Configuración (Pydantic Settings), creación del engine y sesiones de DB, middlewares, logging, seguridad, eventos de arranque, etc.

### 5) Raíz del proyecto
- `main.py`: expone la instancia de `FastAPI` (desde `adapters/http/api.py`).
- `alembic/`: migraciones y configuración de Alembic.
- Docker y dependencias: `Dockerfile`, `docker-compose.yml`, `requirements.txt`.

## Dónde va cada cosa
- Modelos de dominio: `app/domain/entities`.
- Lógica del dominio: `app/domain` (entidades/servicios, reglas).
- Casos de uso: `app/usecases`.
- Modelos ORM (tablas): `app/adapters/db`.
- Repositorios (interfaces): `app/domain`.
- Repositorios (implementaciones): `app/adapters/db/repositories`.
- Controladores/routers HTTP y DTOs externos: `app/adapters/http`.
- Configuración y DB engine/sesiones: `app/core`.
- Migraciones: `alembic/versions`.

## Flujo típico de una petición
1. HTTP entra por `adapters/http` (router/controlador).
2. Se valida y se llama a un caso de uso en `usecases`.
3. El caso de uso interactúa con puertos (interfaces) definidos en `domain`.
4. Las implementaciones concretas de repos viven en `adapters/db` y se inyectan.
5. Se retorna un DTO de respuesta hacia HTTP.

## Alembic y migraciones
- Configuración en `alembic.ini` y `alembic/env.py`.
- `env.py` lee variables de entorno (`APP_DB_*`) vía `app.core.config.get_settings()` y conecta `alembic` a `Base.metadata` para `--autogenerate`.
- Migraciones se guardan en `alembic/versions`.

### Comandos útiles (con Docker Compose)
- Crear nueva migración (autogenerate):
  - `docker compose run --rm api alembic revision --autogenerate -m "add users"`
- Aplicar migraciones:
  - `docker compose run --rm api alembic upgrade head`
- Revertir última:
  - `docker compose run --rm api alembic downgrade -1`
- Ver historial:
  - `docker compose run --rm api alembic history`

Notas:
- `--autogenerate` compara `Base.metadata` vs la base de datos actual.
- Si aún no tienes modelos ORM, crea migraciones vacías con `alembic revision -m "init"` y edita `upgrade/downgrade` manualmente.

## Buenas prácticas
- Mantén el dominio libre de dependencias de frameworks.
- Inyecta dependencias (repos, servicios externos) en los casos de uso.
- Evita lógica de negocio en routers/controladores.
- Aísla modelos ORM de entidades de dominio si sus formas divergen; usa mappers.
- Agrega tests unitarios al dominio y de integración para adapters.
