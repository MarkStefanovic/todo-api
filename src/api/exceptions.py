import fastapi
from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


__all__ = ("CREDENTIALS_EXCEPTION", "http_error_handler")

CREDENTIALS_EXCEPTION = fastapi.HTTPException(
    status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({"errors": [exc.detail]}, status_code=exc.status_code)
