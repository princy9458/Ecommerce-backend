from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# -----------------------
# CREATE (Single Variant)
# -----------------------
class VariantCreate(BaseModel):
    productId: str = Field(..., description="Product ID reference")
    color: str
    size: Optional[str] = None
    sku: Optional[str] = None
    price: float
    stock: int
    isAvailable: bool = True


# -----------------------
# UPDATE (Single Variant)
# -----------------------
class VariantUpdate(BaseModel):
    color: Optional[str] = None
    size: Optional[str] = None
    sku: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    isAvailable: Optional[bool] = None


# -----------------------
# RESPONSE MODEL
# -----------------------
class VariantResponse(BaseModel):
    id: str
    productId: str
    color: str
    size: Optional[str] = None
    sku: Optional[str] = None
    price: float
    stock: int
    isAvailable: bool
    createdAt: datetime


# -----------------------
# BULK CREATE
# -----------------------
class BulkVariantCreate(BaseModel):
    variants: List[VariantCreate]


# -----------------------
# BULK UPDATE
# -----------------------
class BulkVariantUpdateItem(BaseModel):
    variant_id: str
    data: VariantUpdate


class BulkVariantUpdate(BaseModel):
    updates: List[BulkVariantUpdateItem]


# -----------------------
# BULK DELETE
# -----------------------
class BulkVariantDelete(BaseModel):
    variant_ids: List[str]
