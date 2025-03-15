from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Union


async def custom_exception_handler(
    request: Request,
    exc: Union[HTTPException, Exception]
) -> JSONResponse:
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
