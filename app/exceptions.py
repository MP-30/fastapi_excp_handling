from fastapi import HTTPException
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND, 
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR
)

class APIException(HTTPException):
    
    def __init__(
        self, 
        status_code:int = HTTP_500_INTERNAL_SERVER_ERROR,
        detail: str = "An unexcepted error occured",
        error_code: str= "GENERIC ERROR", 
        title: str= None):
        
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code
        self.title = title
        
class BadRequestException(APIException):
    def __init__(
        self, details: str= "Bad Request", error_code: str= "Bad Request", **kwargs
    ):
        super().__init__(status_code=HTTP_400_BAD_REQUEST, detail= details, error_code=error_code, **kwargs)
        
class NotFoundException(APIException):
    def __init__(
        self, details: str= "Resource not found", error_code: str= "Not_found", **kwargs
    ):
        super().__init__(status_code=HTTP_404_NOT_FOUND, detail= details, error_code=error_code, **kwargs)
        
class UnprocessableEntityException(APIException):
    def __init__(
        self, details: str= "Unprocessable entity", error_code: str= "UNPROCESSABLE_ENTITY", **kwargs
    ):
        super().__init__(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail= details, error_code=error_code, **kwargs)
        