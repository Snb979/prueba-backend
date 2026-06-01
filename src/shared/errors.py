from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.shared.responses import envelope


class AppError(Exception):
    def __init__(self, status_code: int, message: str, data=None):
        self.status_code = status_code
        self.message = message
        self.data = data


class UnauthorizedError(AppError):
    def __init__(self, message: str = "Authentication credentials were not provided or are invalid"):
        super().__init__(status.HTTP_401_UNAUTHORIZED, message)


class ForbiddenError(AppError):
    def __init__(self, message: str = "You do not have permission to perform this action"):
        super().__init__(status.HTTP_403_FORBIDDEN, message)


class NotFoundError(AppError):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(status.HTTP_404_NOT_FOUND, message)


class ConflictError(AppError):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(status.HTTP_409_CONFLICT, message)


class BadRequestError(AppError):
    def __init__(self, message: str = "Invalid request"):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=envelope(
                success=False,
                status=exc.status_code,
                message=exc.message,
                data=exc.data,
            ),
        )

    @app.exception_handler(HTTPException)
    async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
        message = exc.detail if isinstance(exc.detail, str) else "Request failed"
        data = None if isinstance(exc.detail, str) else exc.detail
        return JSONResponse(
            status_code=exc.status_code,
            content=envelope(success=False, status=exc.status_code, message=message, data=data),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=envelope(
                success=False,
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                message="Validation error",
                data=exc.errors(),
            ),
        )

    @app.exception_handler(Exception)
    async def unhandled_error_handler(_: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=envelope(
                success=False,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Internal server error",
            ),
        )
