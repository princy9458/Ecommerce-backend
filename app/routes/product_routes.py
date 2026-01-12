from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel

from app.database import product_collection
from app.schemas.product_schema import (
    ProductCreate,
    BulkProductCreate,
    ProductResponse
)

router = APIRouter()


# =====================================================
# CREATE
# =====================================================

@router.post("/")
async def add_product(product: ProductCreate):
    await product_collection.insert_one(product.dict())
    return {"message": "Product added successfully"}


@router.post("/bulk")
async def add_bulk_products(data: BulkProductCreate):
    docs = [product.dict() for product in data.products]
    result = await product_collection.insert_many(docs)
    return {
        "message": "Products added successfully",
        "count": len(result.inserted_ids)
    }


# =====================================================
# READ
# =====================================================

# 🔹 READ ALL
@router.get("/", response_model=List[ProductResponse])
async def get_all_products():
    products = []
    cursor = product_collection.find()

    async for product in cursor:
        products.append({
            "id": str(product["_id"]),
            "name": product["name"],
            "price": product["price"],
            "category": product.get("category"),
            "tags": product.get("tags", []),
            "stock": product.get("stock"),
            "is_active": product.get("is_active", True)
        })

    return products


# 🔹 READ BY ID
@router.get("/{product_id}", response_model=ProductResponse)
async def get_product_by_id(product_id: str):
    product = await product_collection.find_one(
        {"_id": ObjectId(product_id)}
    )

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "price": product["price"],
        "category": product.get("category"),
        "tags": product.get("tags", []),
        "stock": product.get("stock"),
        "is_active": product.get("is_active", True)
    }


# 🔹 BULK READ (FILTER)
@router.get("/filter", response_model=List[ProductResponse])
async def filter_products(
    category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    is_active: Optional[bool] = Query(None)
):
    query = {}

    if category:
        query["category"] = category

    if is_active is not None:
        query["is_active"] = is_active

    if min_price is not None or max_price is not None:
        query["price"] = {}
        if min_price is not None:
            query["price"]["$gte"] = min_price
        if max_price is not None:
            query["price"]["$lte"] = max_price

    products = []
    cursor = product_collection.find(query)

    async for product in cursor:
        products.append({
            "id": str(product["_id"]),
            "name": product["name"],
            "price": product["price"],
            "category": product.get("category"),
            "tags": product.get("tags", []),
            "stock": product.get("stock"),
            "is_active": product.get("is_active", True)
        })

    return products


# =====================================================
# UPDATE
# =====================================================

class ProductUpdate(BaseModel):
    name: Optional[str]
    price: Optional[float]
    category: Optional[str]
    tags: Optional[List[str]]
    stock: Optional[int]
    is_active: Optional[bool]


# 🔹 UPDATE BY ID
@router.put("/{product_id}")
async def update_product(product_id: str, data: ProductUpdate):
    update_data = {k: v for k, v in data.dict().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No data to update")

    result = await product_collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product updated successfully"}


# 🔹 BULK UPDATE
@router.put("/bulk-update")
async def bulk_update_products(
    category: str,
    is_active: Optional[bool] = None,
    stock: Optional[int] = None
):
    update_data = {}

    if is_active is not None:
        update_data["is_active"] = is_active

    if stock is not None:
        update_data["stock"] = stock

    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")

    result = await product_collection.update_many(
        {"category": category},
        {"$set": update_data}
    )

    return {
        "matched": result.matched_count,
        "updated": result.modified_count
    }


# =====================================================
# DELETE
# =====================================================

# 🔹 DELETE BY ID
@router.delete("/{product_id}")
async def delete_product(product_id: str):
    result = await product_collection.delete_one(
        {"_id": ObjectId(product_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product deleted successfully"}


# 🔹 BULK DELETE
@router.delete("/bulk-delete")
async def bulk_delete_products(
    category: Optional[str] = None,
    is_active: Optional[bool] = None
):
    query = {}

    if category:
        query["category"] = category

    if is_active is not None:
        query["is_active"] = is_active

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Provide at least one filter"
        )

    result = await product_collection.delete_many(query)

    return {"deleted_count": result.deleted_count}
