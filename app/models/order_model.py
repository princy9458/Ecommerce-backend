from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class OrderItem(BaseModel):
    product_id: str
    product_name: str
    price: float
    quantity: int
    total_price: float


class OrderModel(BaseModel):
    order_id: str
    user_id: str
    items: List[OrderItem]
    total_amount: float
    payment_method: str
    status: str
    order_date: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        extra = "forbid"  
