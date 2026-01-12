from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId


class ProductModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    description: Optional[str] = None
    price: float
    category: str
    tags: List[str] = []
    stock: int
    is_active: bool = True

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
