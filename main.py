from fastapi import FastAPI
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app=FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

@app.get("/items")
def get_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.get("/products")
def get_products(category: Optional[str] = None):
    if category:
        return {"category": category}
    return {"message": "showing all products"}

@app.get("/users/{user_id}/orders")
def get_user_orders(user_id: int, limit: int = 5, status: Optional[str] = None):
    return {
        "user_id": user_id,
        "limit": limit,
        "status": status
    }

@app.get("/products/{product_id}")
def get_product_id(product_id:int, discount: float=0.0):
    return{"product_id":product_id, "discount": discount}

@app.get("/orders")
def orders(status:Optional[str]=None, limit: int = 10):
    return {"status":status, "limit":limit}

from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    in_stock: bool=True
    description: Optional[str] = None


@app.post("/items")
def create_item(item: Item):
    return item

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    name: str
    email: str

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    return user