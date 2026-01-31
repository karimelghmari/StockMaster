from pydantic import BaseModel,ConfigDict
from datetime import datetime
from enum import Enum
from typing import Optional
class TransactionType(str,Enum):
    sale="sale"
    restock="restock"
class ProductBase(BaseModel):
    name: str
    price: float
    description: str | None = None
    quantity: int
    min_stock_level: int=5
class ProductCreate(ProductBase):
    pass
class Product(ProductBase):
    id: int
    class config:
        from_attributes=True
class TransactionBase(BaseModel):
    product_id:int
    quantity:int
    type:TransactionType
class TransactionCreate(TransactionBase):
    pass
class Transaction(TransactionBase):
    id:int
    date:datetime
    product:Product
    class config:
        from_attributes=True
class UserCreate(BaseModel):
    username:str
    password:str
class UserOut(BaseModel):
    id:int
    username:str
    is_active:bool
    model_config = ConfigDict(from_attributes=True)
class Token(BaseModel):
    access_token:str
    token_type:str
class TokenData(BaseModel):
    username:str|None=None
class DashboardStats(BaseModel):
    total_products: int
    total_inventory_value: float
    low_stock_count: int
    total_transactions: int
    low_stock_items: list[Product]
    
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    min_stock_level: Optional[int] = None
