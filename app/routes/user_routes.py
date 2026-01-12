from fastapi import APIRouter, HTTPException
from app.database import user_collection
from app.schemas.user_schema import UserCreate
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/signup")
async def signup(user: UserCreate):
    try:
        # email already exists?
        existing_user = await user_collection.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = pwd_context.hash(user.password)

        new_user = {
            "name": user.name,
            "email": user.email,
            "password": hashed_password
        }

        await user_collection.insert_one(new_user)

        return {"message": "User created successfully"}

    except Exception as e:
        print("SIGNUP ERROR 👉", e)  # IMPORTANT
        raise HTTPException(status_code=500, detail="Internal Server Error")