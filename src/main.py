from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import get_settings
from src.core.logging import RequestLoggingMiddleware, configure_logging
from src.db.base import Base
from src.db.session import engine
from src.modules.auth.router import router as auth_router
from src.modules.users.router import router as users_router
from src.modules.vehicles.router import router as vehicles_router
from src.shared.errors import register_exception_handlers
from src.shared.responses import ok

# Import models so SQLAlchemy registers metadata and relationships.
from src.modules.users import models as user_models  # noqa: F401
from src.modules.vehicles import models as vehicle_models  # noqa: F401

configure_logging()
settings = get_settings()

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)

register_exception_handlers(app)

app.include_router(auth_router, prefix=settings.api_prefix)
app.include_router(users_router, prefix=settings.api_prefix)
app.include_router(vehicles_router, prefix=settings.api_prefix)


@app.on_event("startup")
def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return ok("Backend running successfully")
