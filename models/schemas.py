from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

# ─── Item ─────────────────────────────────────────────────
class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True
    description: Optional[str] = None

# ─── Product ──────────────────────────────────────────────
class Product(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    description: Optional[str] = Field(None, max_length=200)

# ─── User ─────────────────────────────────────────────────
class UserCreate(BaseModel):
    name: str = Field(min_length=2)
    email: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

# ─── Student ──────────────────────────────────────────────
class StudentCreate(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(ge=18, le=30)
    email: str
    password: str = Field(min_length=8)

class StudentResponse(BaseModel):
    name: str
    age: int
    email: str

# ─── Book ─────────────────────────────────────────────────
class Book(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    author: str = Field(min_length=2)
    price: float = Field(gt=0)
    in_stock: bool = True
    description: Optional[str] = None

# ─── Address, Company, Employee ───────────────────────────
class Address(BaseModel):
    city: str
    country: str
    pincode: str

class Company(BaseModel):
    name: str = Field(min_length=2)
    email: str
    phone: str
    address: Address

class Employee(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(ge=18, le=60)
    salary: float = Field(gt=0)
    company: Company

class Customer(BaseModel):
    name: str = Field(min_length=2)
    email: str
    address: Address

class OrderItem(BaseModel):
    name: str
    price: float = Field(gt=0)
    quantity: int = Field(ge=1)

class Cart(BaseModel):
    user_id: int
    items: list[OrderItem]
    coupon: Optional[str] = None

# ─── Order Status Enum ────────────────────────────────────
class OrderStatus(str, Enum):
    pending = "pending"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"