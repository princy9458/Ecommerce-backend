from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import (
    user_routes,
    product_routes,
    category_routes,
    order_routes,
    variant_routes
)

app = FastAPI(
    title="E-Commerce API",
    description="E-Commerce Backend using FastAPI & MongoDB",
    version="1.0.0"
)

# -----------------------
# CORS
# -----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# ROUTERS
# -----------------------
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(category_routes.router, prefix="/categories", tags=["Categories"])
app.include_router(product_routes.router, prefix="/products", tags=["Products"])
app.include_router(order_routes.router, prefix="/orders", tags=["Orders"])
app.include_router(variant_routes.router, prefix="/variants", tags=["Variants"]) 

# -----------------------
# ROOT CHECK API
# -----------------------
@app.get("/")
async def root():
    return {
        "message": "E-Commerce API is running successfully 🚀"
    }
