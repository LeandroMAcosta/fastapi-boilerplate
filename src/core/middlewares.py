from typing import Union

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


async def custom_exception_handler(request: Request, exc: Union[HTTPException, Exception]) -> JSONResponse:
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail, "status": exc.status_code},
        )
    # Handle other types of exceptions
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "status": 500},
    )
