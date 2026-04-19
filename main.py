from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

app = FastAPI(
    title="FastAPI Learning Project",
    description="Learning FastAPI from scratch with Kasish",
    version="1.0.0"
)

# ─── Fake Database ───────────────────────────────────────
fake_users_db = {}

# ─── Models ──────────────────────────────────────────────
class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True
    description: Optional[str] = None

class Product(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    description: Optional[str] = Field(None, max_length=200)

class UserCreate(BaseModel):
    name: str = Field(min_length=2)
    email: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class StudentCreate(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(ge=18, le=30)
    email: str
    password: str = Field(min_length=8)

class StudentResponse(BaseModel):
    name: str
    age: int
    email: str

class Book(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    author: str = Field(min_length=2)
    price: float = Field(gt=0)
    in_stock: bool = True
    description: Optional[str] = None

class OrderStatus(str, Enum):
    pending = "pending"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

# ─── Root ─────────────────────────────────────────────────
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Hello, FastAPI!"}

# ─── Items ────────────────────────────────────────────────
@app.get("/items", tags=["Items"])
def get_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.post("/items", tags=["Items"])
def create_item(item: Item):
    return item

# ─── Products ─────────────────────────────────────────────
@app.get("/products", tags=["Products"])
def get_products(category: Optional[str] = None):
    if category:
        return {"category": category}
    return {"message": "showing all products"}

@app.post("/products", tags=["Products"])
def create_product(product: Product):
    return product

@app.get("/products/{product_id}", tags=["Products"])
def get_product_id(product_id: int, discount: float = 0.0):
    return {"product_id": product_id, "discount": discount}

# ─── Orders ───────────────────────────────────────────────
@app.get("/orders", tags=["Orders"])
def orders(status: Optional[str] = None, limit: int = 10):
    return {"status": status, "limit": limit}

# ─── Users ────────────────────────────────────────────────
@app.get("/users", tags=["Users"])
def get_users():
    return fake_users_db

@app.post("/users", status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_user(user: UserCreate):
    user_id = len(fake_users_db) + 1
    fake_users_db[user_id] = user
    return {"id": user_id, **user.model_dump()}

@app.get("/users/{user_id}", tags=["Users"])
def get_user(user_id: int):
    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return fake_users_db[user_id]

@app.put("/users/{user_id}", tags=["Users"])
def update_user(user_id: int, user: UserCreate):
    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    fake_users_db[user_id] = user
    return {"id": user_id, **user.model_dump()}

@app.patch("/users/{user_id}", tags=["Users"])
def partial_update_user(user_id: int, user: UserUpdate):
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

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
def delete_user(user_id: int):
    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    del fake_users_db[user_id]

@app.get("/users/{user_id}/orders", tags=["Users"])
def get_user_orders(user_id: int, limit: int = 5, status: Optional[str] = None):
    return {"user_id": user_id, "limit": limit, "status": status}

# ─── Books ────────────────────────────────────────────────
@app.get("/books/{book_id}", tags=["Books"])
def books(book_id: int, include_reviews: bool = False):
    return {"book_id": book_id, "include_reviews": include_reviews}

@app.post("/books", tags=["Books"])
def books_details(book: Book):
    return book

# ─── Students ─────────────────────────────────────────────
@app.post("/students", response_model=StudentResponse, tags=["Students"])
def StudentDetails(student: StudentCreate):
    return student

@app.get("/orders/status/{status}", tags=["Orders"])
def get_orders_by_status(status: OrderStatus):
    if status == OrderStatus.pending:
        return {"status": status, "message": "Order is being processed"}
    elif status == OrderStatus.shipped:
        return {"status": status, "message": "Order is on the way!"}
    elif status == OrderStatus.delivered:
        return {"status": status, "message": "Order delivered!"}
    else:
        return {"status": status, "message": "Order was cancelled"}