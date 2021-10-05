from fastapi import FastAPI, HTTPException, status, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.params import Depends
from sqlalchemy import text
from starlette import requests
from starlette.responses import JSONResponse
from app.models import item as item_model
from app.schemas import item as item_schemas
from sqlalchemy.orm import Session
from app.database import get_db


def show_all(db: Session = Depends(get_db)):
    items = db.query(item_model.Item).all()
    return items


def show(id: int, db: Session = Depends(get_db)):
    item = db.query(item_model.Item).filter(item_model.Item.id == id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item with id {id} not found")
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(item))


def create(req: item_schemas.Item, db: Session = Depends(get_db)):
    new_item = item_model.Item(name=req.name, stock=req.stock)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    res = {'message': 'Item Created', 'data': new_item}
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(res))


def update_stock(id: int, req: item_schemas.UpdateStock, db: Session = Depends(get_db)):
    with db.begin():
        item = db.query(item_model.Item).filter(item_model.Item.id == id)
        result = item.first().stock - req.stock
        if not item.first():
            db.rollback()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Item with id {id} not found")

        if item.first().stock <= 0 or result < 0:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Item with id {id} out of stock")
        item.update({
            "stock": result
        })
        db.commit()
    res = {
        'message': 'Item Updated'
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(res))


def update_stock_race(id: int, req: item_schemas.UpdateStock, db: Session = Depends(get_db)):
    item = db.execute(
        text("select stock from items where id=:x"), [{"x": id}])

    result = 0
    for row in item:
        result = row['stock'] - req.stock
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item with id {id} not found")

    if result <= 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item with id {id} out of stock")
    db.execute(
        text(
            "UPDATE items SET stock=stock-:y WHERE id=:x"), [{"y": req.stock, "x": id}]
    )

    db.commit()

    res = {
        'message': 'Item Updated'
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(res))


def update(id: int, req: item_schemas.Item, db: Session = Depends(get_db)):
    item = db.query(item_model.Item).filter(item_model.Item.id == id)

    if not item.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item with id {id} not found")

    item.update({
        "name": req.name,
        "stock": req.stock
    })
    db.commit()
    res = {
        'message': 'Item Updated'
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(res))


def destroy(id: int, db: Session = Depends(get_db)):
    item = db.query(item_model.Item).filter(item_model.Item.id == id)

    if not item.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item with id {id} not found")
    item.delete(synchronize_session=False)
    db.commit()
    res = {
        'message': 'Item Deleted'
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(res))
