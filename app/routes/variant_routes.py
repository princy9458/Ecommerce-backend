from fastapi import APIRouter, HTTPException
from bson import ObjectId
from datetime import datetime

from app.database import variant_collection, product_collection
from app.models.variant_model import (
    VariantCreate,
    VariantUpdate,
    BulkVariantCreate,
    BulkVariantUpdate,
    BulkVariantDelete
)

router = APIRouter(
    prefix="/variants",
    tags=["Variants"]
)

# -------------------------------------------------
# 🔹 HELPER: ObjectId Validation
# -------------------------------------------------
def validate_object_id(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid ObjectId format: {id}"
        )
    return ObjectId(id)


# -------------------------------------------------
# CREATE SINGLE VARIANT
# -------------------------------------------------
@router.post("/")
async def create_variant(variant: VariantCreate):
    product_id = validate_object_id(variant.productId)

    product = await product_collection.find_one({"_id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    data = variant.dict()
    data["productId"] = product_id
    data["createdAt"] = datetime.utcnow()

    result = await variant_collection.insert_one(data)

    data["_id"] = str(result.inserted_id)
    data["productId"] = str(data["productId"])

    return data


# -------------------------------------------------
# BULK CREATE VARIANTS
# -------------------------------------------------
@router.post("/bulk-create")
async def bulk_create_variants(payload: BulkVariantCreate):
    insert_data = []

    for variant in payload.variants:
        product_id = validate_object_id(variant.productId)

        product = await product_collection.find_one({"_id": product_id})
        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product not found for ID {variant.productId}"
            )

        data = variant.dict()
        data["productId"] = product_id
        data["createdAt"] = datetime.utcnow()
        insert_data.append(data)

    result = await variant_collection.insert_many(insert_data)

    return {
        "message": "Variants created successfully ✅",
        "inserted_ids": [str(_id) for _id in result.inserted_ids]
    }


# -------------------------------------------------
# GET VARIANTS BY PRODUCT
# -------------------------------------------------
@router.get("/{product_id}")
async def get_variants_by_product(product_id: str):
    product_obj_id = validate_object_id(product_id)

    variants = []
    async for v in variant_collection.find({"productId": product_obj_id}):
        v["_id"] = str(v["_id"])
        v["productId"] = str(v["productId"])
        variants.append(v)

    return variants


# -------------------------------------------------
# UPDATE SINGLE VARIANT
# -------------------------------------------------
@router.put("/{variant_id}")
async def update_variant(variant_id: str, data: VariantUpdate):
    variant_obj_id = validate_object_id(variant_id)

    update_data = {k: v for k, v in data.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided to update")

    result = await variant_collection.update_one(
        {"_id": variant_obj_id},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Variant not found")

    return {"message": "Variant updated successfully ✅"}


# -------------------------------------------------
# BULK UPDATE VARIANTS
# -------------------------------------------------
@router.put("/bulk-update")
async def bulk_update_variants(payload: BulkVariantUpdate):
    updated = 0

    for item in payload.updates:
        variant_obj_id = validate_object_id(item.variant_id)

        update_data = {
            k: v for k, v in item.data.dict().items() if v is not None
        }
        if not update_data:
            continue

        result = await variant_collection.update_one(
            {"_id": variant_obj_id},
            {"$set": update_data}
        )

        if result.matched_count:
            updated += 1

    return {
        "message": "Bulk update completed ✅",
        "updated_count": updated
    }


# -------------------------------------------------
# DELETE SINGLE VARIANT
# -------------------------------------------------
@router.delete("/{variant_id}")
async def delete_variant(variant_id: str):
    variant_obj_id = validate_object_id(variant_id)

    result = await variant_collection.delete_one({"_id": variant_obj_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Variant not found")

    return {"message": "Variant deleted successfully ❌"}


# -------------------------------------------------
# BULK DELETE VARIANTS
# -------------------------------------------------
@router.delete("/bulk-delete")
async def bulk_delete_variants(payload: BulkVariantDelete):
    object_ids = [validate_object_id(v_id) for v_id in payload.variant_ids]

    result = await variant_collection.delete_many(
        {"_id": {"$in": object_ids}}
    )

    return {
        "message": "Bulk delete completed ❌",
        "deleted_count": result.deleted_count
    }
