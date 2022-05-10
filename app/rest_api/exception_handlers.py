from http import HTTPStatus

from fastapi import Request
from starlette.responses import JSONResponse

from app.core.shared.exception.base_exceptions import EntityNotFoundException, InvalidStatusException
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
