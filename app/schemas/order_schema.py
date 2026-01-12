from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

# -------------------
# ORDER ITEM
# -------------------
class OrderItem(BaseModel):
    product_id: str
    quantity: int
    price: float

# -------------------
# CREATE ORDER
# -------------------
class OrderCreate(BaseModel):
    user_id: str
    items: List[OrderItem]
    total_amount: float
    status: Optional[str] = "pending"

# -------------------
# BULK CREATE
# -------------------
class BulkOrderCreate(BaseModel):
    orders: List[OrderCreate]

# -------------------
# RESPONSE MODEL
# -------------------
class OrderResponse(BaseModel):
    id: Optional[str] = Field(alias="_id")
    user_id: str
    items: List[OrderItem]
    total_amount: float
    status: str

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
