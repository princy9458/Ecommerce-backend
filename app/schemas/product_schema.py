from pydantic import BaseModel
from typing import List, Optional


# -------------------
# POST (Create)
# -------------------
class ProductCreate(BaseModel):
    name: str
    price: float
    category: str
    tags: List[str]
    stock: int


# -------------------
# POST (Bulk Create)
# -------------------
class BulkProductCreate(BaseModel):
    products: List[ProductCreate]


# -------------------
# GET (Response)
# -------------------
class ProductResponse(BaseModel):
    id: str
    name: str
    price: float
    category: str
    tags: Optional[List[str]] = []
    stock: int
    is_active: Optional[bool] = True

