from fastapi import FastAPI, HTTPException, status, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.params import Depends
from starlette import requests
from starlette.responses import JSONResponse
from app import routers
from app.models import item as item_model
from app.schemas import item as item_schemas
from sqlalchemy.orm import Session
from ..database import get_db
from ..repository import item
route = APIRouter(
    prefix="/items",
    tags=['Items']
)


@route.get('/')
def get_all(db: Session = Depends(get_db)):
    return item.show_all(db)


@route.get('/{id}')
def get_item(id: int, db: Session = Depends(get_db)):
    return item.show(id, db)


@route.post('/')
def create(req: item_schemas.Item, db: Session = Depends(get_db)):
    return item.create(req, db)


@route.put('/{id}')
def update(id: int, req: item_schemas.Item, db: Session = Depends(get_db)):
    return item.update(id, req, db)


@route.patch('/{id}/checkout')
def update_stock(id: int, req: item_schemas.UpdateStock, db: Session = Depends(get_db)):
    return item.update_stock(id, req, db)


@route.delete('/{id}')
def destroy(id: int, db: Session = Depends(get_db)):

    return item.destroy(id, db)
