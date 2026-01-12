from fastapi import APIRouter, HTTPException
from bson import ObjectId
from typing import List

from app.database import category_collection
from app.schemas.category_schema import (
    CategoryCreate,
    BulkCategoryCreate,
    CategoryModel
)

router = APIRouter(prefix="/categories", tags=["Categories"])

# -------------------
# CREATE (Single)
# -------------------
@router.post("/")
async def create_category(category: CategoryCreate):
    await category_collection.insert_one(category.dict())
    return {"message": "Category created successfully"}

# -------------------
# CREATE (Bulk)
# -------------------
@router.post("/bulk")
async def create_bulk_categories(data: BulkCategoryCreate):
    docs = [{"name": name} for name in data.categories]
    result = await category_collection.insert_many(docs)
    return {
        "message": "Bulk categories added",
        "count": len(result.inserted_ids)
    }

# -------------------
# READ (All)
# -------------------
@router.get("/", response_model=List[CategoryModel])
async def get_all_categories():
    categories = []
    async for cat in category_collection.find():
        categories.append(cat)
    return categories

# -------------------
# READ (By ID)
# -------------------
@router.get("/{category_id}", response_model=CategoryModel)
async def get_category_by_id(category_id: str):
    if not ObjectId.is_valid(category_id):
        raise HTTPException(status_code=400, detail="Invalid category id")

    category = await category_collection.find_one(
        {"_id": ObjectId(category_id)}
    )
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return category

# -------------------
# UPDATE
# -------------------
@router.put("/{category_id}")
async def update_category(category_id: str, category: CategoryCreate):
    result = await category_collection.update_one(
        {"_id": ObjectId(category_id)},
        {"$set": category.dict()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")

    return {"message": "Category updated successfully"}

# -------------------
# DELETE
# -------------------
@router.delete("/{category_id}")
async def delete_category(category_id: str):
    result = await category_collection.delete_one(
        {"_id": ObjectId(category_id)}
    )
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")

    return {"message": "Category deleted successfully"}
