from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId

from fastapi.responses import StreamingResponse
import csv
from io import StringIO

from app.database import order_collection
from app.models.order_model import OrderModel


router = APIRouter(prefix="/orders", tags=["Orders"])

# -------------------
# CREATE (Single)
# -------------------
@router.post("/place-order")
async def place_order(order: OrderModel):
    await order_collection.insert_one(order.dict(by_alias=True))
    return {
        "message": "Order placed successfully",
        "order_id": order.order_id
    }

# -------------------
# READ (All)
# -------------------
@router.get("/", response_model=List[OrderModel])
async def get_all_orders():
    orders = []
    async for order in order_collection.find():
        orders.append(order)
    return orders

# -------------------
# READ (By Mongo ID)
# -------------------
@router.get("/{order_id}", response_model=OrderModel)
async def get_order_by_id(order_id: str):
    if not ObjectId.is_valid(order_id):
        raise HTTPException(status_code=400, detail="Invalid order id")

    order = await order_collection.find_one(
        {"_id": ObjectId(order_id)}
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order

# -------------------
# UPDATE (Full Order)
# -------------------
@router.put("/{order_id}")
async def update_order(order_id: str, order: OrderModel):
    result = await order_collection.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": order.dict(exclude={"id"}, by_alias=True)}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")

    return {"message": "Order updated successfully"}

# -------------------
# DELETE
# -------------------
@router.delete("/{order_id}")
async def delete_order(order_id: str):
    result = await order_collection.delete_one(
        {"_id": ObjectId(order_id)}
    )
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")

    return {"message": "Order deleted successfully"}

# =================================================
# EXPORT ORDERS TO CSV  (🔥 Boss-impress feature)
# =================================================
@router.get("/export/csv")
async def export_orders_csv():
    orders = []
    async for order in order_collection.find({}, {"_id": 0}):
        orders.append(order)

    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=orders[0].keys())
    writer.writeheader()
    writer.writerows(orders)

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=orders.csv"
        }
    )

