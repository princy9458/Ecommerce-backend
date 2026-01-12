from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"

client = AsyncIOMotorClient(MONGO_URL)

db = client.ecommerce_db

# -----------------------
# Collections
# -----------------------
user_collection = db.users
product_collection = db.products
category_collection = db.categories
order_collection = db.orders
variant_collection = db.product_variants
