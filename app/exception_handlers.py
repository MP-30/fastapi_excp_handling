from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from starlette.status import (
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_422_UNPROCESSABLE_ENTITY, 
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)
from app.exceptions import APIException

async def api_exception_handler(request: Request, exc: APIException):
    
    problem_details = {
        "status": exc.status_code,
        "detail": exc.detail,
        "title": exc.title,
        "code": exc.error_code
    }
    
    return JSONResponse(status_code=exc.status_code, content=problem_details)


async def http_exception_handler(request: Request, exc: HTTPException):
    
    problem_details = {
        "type": f"/errors/http_{exc.status_code}",
        "title": exc.title,
        "status": exc.status_code,
        "detail": exc.detail,
        "instance": str(request.url),
    }
    
    return JSONResponse(status_code=exc.status_code, content=problem_details)

async def generic_exceptopn_handler(request: Request, exc: Exception):
    problem_details = {
        "type": "/errors/internal_server_error",
        "title":"Internal Server Error",
        "status": HTTP_500_INTERNAL_SERVER_ERROR,
        "details": "An unexpected server occurred. Please try again later.",
        "instance": str(request.url)
    }
    
    return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR)

def register_exception_handlers(app:FastAPI):
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(APIException, api_exception_handler)
    app.add_exception_handler(Exception, generic_exceptopn_handler)