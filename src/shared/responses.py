from typing import Any


def envelope(
    *,
    success: bool,
    status: int,
    message: str,
    data: Any = None,
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "success": success,
        "status": status,
        "message": message,
        "data": data,
        "meta": meta or {},
    }


def ok(message: str, data: Any = None, meta: dict[str, Any] | None = None, status: int = 200):
    return envelope(success=True, status=status, message=message, data=data, meta=meta)
