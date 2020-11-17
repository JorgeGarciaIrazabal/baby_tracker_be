import os
from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.routing import Mount

from src.models import Base

static_path = Path(__file__).parent / "dist/static"
engine_url = os.environ.get("DATABASE_URL", "postgresql://flatiron:flatiron@localhost:6432/data")
engine = create_engine(engine_url)
app = FastAPI()
Session: sessionmaker = sessionmaker(bind=engine)

Base.metadata.create_all(engine)
Session.configure(bind=engine)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Baby Tracker",
        version="0.1.0",
        description="Track everything your baby does",
        routes=app.routes,
    )

    # Custom documentation fastapi-jwt-auth
    headers = {
        "name": "Authorization",
        "in": "header",
        "required": False,
        "schema": {
            "title": "Authorization",
            "type": "string"
        },
    }

    # Get routes from index 4 because before that fastapi define router for /openapi.json, /redoc, /docs, etc
    # Get all router where operation_id is authorize
    router_authorize = [route for route in app.routes[4:] if not isinstance(route, Mount) and "api" in route.tags]
    testCount = 0
    for route in router_authorize:
        method = list(route.methods)[0].lower()
        try:
            # If the router has another parameter
            openapi_schema["paths"][route.path][method]['operationId'] = route.name
            openapi_schema["paths"][route.path][method]['parameters'].append(headers)
        except Exception:
            # If the router doesn't have a parameter
            openapi_schema["paths"][route.path][method].update({"parameters":[headers]})
        testCount += 1

    app.openapi_schema = openapi_schema
    return app.openapi_schema


def get_db() -> Session:
    db = Session()
    try:
        yield db
    finally:
        db.close()
