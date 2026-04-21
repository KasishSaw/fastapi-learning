from fastapi import APIRouter, HTTPException, status, Depends
from models.schemas import UserCreate, UserUpdate
from dependencies import verify_token

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

fake_users_db = {}

@router.get("")
async def get_users():
    return fake_users_db

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    user_id = len(fake_users_db) + 1
    fake_users_db[user_id] = user
    return {"id": user_id, **user.model_dump()}

@router.get("/{user_id}")
async def get_user(user_id: int):
    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return fake_users_db[user_id]

@router.put("/{user_id}")
async def update_user(user_id: int, user: UserCreate):
    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    fake_users_db[user_id] = user
    return {"id": user_id, **user.model_dump()}

@router.patch("/{user_id}")
async def partial_update_user(user_id: int, user: UserUpdate):
    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    stored_user = fake_users_db[user_id].model_dump()
    update_data = user.model_dump(exclude_unset=True)
    stored_user.update(update_data)
    fake_users_db[user_id] = UserCreate(**stored_user)
    return {"id": user_id, **stored_user}

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    del fake_users_db[user_id]

@router.get("/{user_id}/orders")
async def get_user_orders(user_id: int, limit: int = 5, status: str = None):
    return {"user_id": user_id, "limit": limit, "status": status}

@router.get("/{user_id}/profile")
async def get_user_profile(user_id: int):
    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {**fake_users_db[user_id].model_dump(), "profile_views": 100}