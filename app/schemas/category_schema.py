from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

class CategoryCreate(BaseModel):
    name: str

class BulkCategoryCreate(BaseModel):
    categories: List[str]

class CategoryModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name: str

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
