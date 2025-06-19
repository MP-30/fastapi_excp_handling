from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg
from psycopg.rows import dict_row
from . import schemas, utils, models
from .database import engine, get_db
import time
from sqlalchemy.orm import Session
from .routers import basic_curd
from .exception_handlers import (
    api_exception_handler,
    http_exception_handler,
    generic_exceptopn_handler,
    register_exception_handlers
)
from .exceptions import APIException
from fastapi import HTTPException


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

register_exception_handlers(app)


while True:
    try:
        conn = psycopg.connect(host = 'localhost', dbname = 'for_wsl_fastapi_excep_handling', user='postgres', password = 'singh', row_factory=dict_row )
        
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as e: 
        print('Database connection failed', e)
        time.sleep(2)
        
        
        
@app.get("/")
def root(db: Session = Depends(get_db)):
    
    return {"message" : "Hello World"}

app.include_router(basic_curd.router)