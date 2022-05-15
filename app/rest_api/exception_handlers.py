from http import HTTPStatus

from fastapi import Request
from starlette.responses import JSONResponse

from app.core.shared.exception.base_exceptions import EntityNotFoundException, InvalidStatusException, AuthException
from config.logger import log, LogLevel


async def entity_not_found_exception_handler(request: Request, exception: EntityNotFoundException):
    log(message="Entity not found", log_level=LogLevel.WARNING, exception=exception)
    return JSONResponse(
        status_code=HTTPStatus.NOT_FOUND,
        content={"message": "Entity not found"},
    )


async def invalid_status_exception_handler(request: Request, exception: InvalidStatusException):
    log(message="Invalid status exception", log_level=LogLevel.WARNING, exception=exception)
    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        content={"message": "Entity in invalid status"},
    )


async def entity_persist_exception_handler(request: Request, exception: InvalidStatusException):
    log(message="Entity persist exception", log_level=LogLevel.ERROR, exception=exception)
    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        content={"message": "Error creating the resource"},
    )


async def auth_exception_handler(request: Request, exception: AuthException):
    log(message="User auth exception", log_level=LogLevel.ERROR, exception=exception)
    return JSONResponse(
        status_code=HTTPStatus.UNAUTHORIZED,
        content={"message": exception.message},
        headers={"WWW-Authenticate": "Bearer"},
    )
