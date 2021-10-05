from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    name:  Optional[str] = None
    stock: Optional[int] = None

class Item(ItemBase):
    class Config():
        orm_mode = True

class UpdateStock(ItemBase):
    stock: int

