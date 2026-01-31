from sqlalchemy import Column,Integer,String,Float,ForeignKey,DateTime,Boolean
from sqlalchemy.sql import func
from .database import Base
from sqlalchemy.orm import relationship
class Product(Base):
    __tablename__="products"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    price=Column(Float)
    description = Column(String, nullable=True)
    quantity=Column(Integer)
    min_stock_level=Column(Integer)
    transaction=relationship("Transaction",back_populates="product")
class Transaction(Base):
    __tablename__="transactions"
    id=Column(Integer,primary_key=True,index=True)
    product_id=Column(Integer,ForeignKey("products.id"))
    quantity=Column(Integer)
    type=Column(String)
    date=Column(DateTime(timezone=True),server_default=func.now())
    product=relationship("Product",back_populates="transaction")
class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,unique=True,index=True,nullable=False)
    hashed_password=Column(String,nullable=False)
    is_active=Column(Boolean,default=True)
    