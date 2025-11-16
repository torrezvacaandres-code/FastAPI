from fastapi import FastAPI
from sqlalchemy import text

from app.core.database import get_engine


def create_app() -> FastAPI:
    app = FastAPI(title="FastAPI Hexagonal Skeleton")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/db-check")
    def db_check() -> dict[str, str]:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"database": "ok"}

    return app


app = create_app()
