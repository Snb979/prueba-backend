import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("api.requests")


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        user_id = getattr(request.state, "user_id", None)
        user_role = getattr(request.state, "user_role", None)
        logger.info(
            "%s %s -> %s user_id=%s role=%s duration_ms=%s",
            request.method,
            request.url.path,
            response.status_code,
            user_id or "anonymous",
            user_role or "anonymous",
            duration_ms,
        )
        return response
