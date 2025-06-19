from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. database import engine, get_db
from typing import Optional, List

from app.exceptions import (
    APIException,
    BadRequestException,
    NotFoundException,
    UnprocessableEntityException,
)

from app.exception_handlers import register_exception_handlers


router = APIRouter(
    prefix='/for_curd',
    tags=['Curd']
)

@router.get("/", response_model= List[schemas.BasicCurd])
def get_basic_curd(db:Session= Depends(get_db)):
    curds = db.query(models.curd_table).all()
    print(f"this is for basic curd {curds}")
    
    return curds

@router.get("/{id}", response_model=schemas.BasicCurd)
def get_one_curd(id:int ,db:Session=Depends(get_db)):
    if id <= 0:
        raise BadRequestException(details='Item id cannot be zero', error_code="ITEM_ID_INVALID")
    elif id == 3:
        raise UnprocessableEntityException(details='Id must be integer', error_code="ID_NOT_INTEGER")
    elif id > 100:
        raise NotFoundException(details="ID out of range", error_code="ID_OUT_OF_BOUND")
    single_curd = db.query(models.curd_table).filter(models.curd_table.id== id).first()
    
    print(f"This is single curd{single_curd}")
    
    return single_curd


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.BasicCurd)
def create_curd(post: schemas.BasicCurd, db:Session=Depends(get_db)):
    new_curd = models.curd_table(**post.model_dump())
    db.add(new_curd)
    db.commit()
    db.refresh()
    
    print(f"This data added {new_curd}")
    
    return new_curd


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session=Depends(get_db)):
    
    delete_curd = db.query(models.curd_table).filter(models.curd_table.id== id)
    
    if delete_post.first() == None:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, details=f"Data with {id} does not exits")
    
    delete_curd.delete(synchronize_session=False)
    db.commit()
    db.refresh()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}')
def update_curd(id:int, post: schemas.BasicCurd, db: Session=Depends(get_db)):
    
    update_curd_query = db.query(models.curd_table).filter(models.curd_table.id == id)
    
    update_curd = update_curd_query.first()
    
    if update_curd == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details=f"Data with id : {id} not found")
    
    update_curd_query.update(post.model_dump(), synchronize_session=False)
    
    db.commit()
    
    return update_curd_query.first()