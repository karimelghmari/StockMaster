from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import schemas, models
from ..crud import product_crud
from .auth import get_current_user

router=APIRouter(prefix="/products",tags=["Products"])
#create product
@router.post("/",response_model=schemas.Product)
def create_product(product:schemas.ProductCreate,db:Session=Depends(get_db),current_user:models.User=Depends(get_current_user)):
    return product_crud.create_product(db=db,product=product)
#update product
@router.put("/{product_id}",response_model=schemas.Product)
def update_product(product_id:int,product:schemas.ProductUpdate,db:Session=Depends(get_db),current_user: models.User = Depends(get_current_user)):
    db_product=product_crud.update_product(db=db,product_id=product_id,product=product)
    if db_product is None:
        raise HTTPException(status_code=404,detail="Item not found")
    return db_product
#delete product
@router.delete("/{product_id}")
def delete_product(product_id:int,db:Session=Depends(get_db),current_user: models.User = Depends(get_current_user)):
    db_product=product_crud.delete_product(db=db,product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404,detail="Item not found")
    return {"message":"Item was successfully deleted"}

#read product
@router.get("/",response_model=List[schemas.Product])
def read_product(skip:int=0,limit:int=100,db:Session=Depends(get_db)):
    products=product_crud.get_products(db,skip=skip,limit=limit,)
    return products

#test endpoint
@router.get("/{product_id}",response_model=schemas.Product)
def read_product(product_id:int,db:Session=Depends(get_db)):
    product=product_crud.get_product(db,product_id)
    if product is None:
        raise HTTPException(status_code=404,detail="Item not found")
    return product
#dashboard
@router.get("/dashboard/summary", response_model=schemas.DashboardStats)
def get_summary(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # On appelle simplement notre fonction CRUD
    return product_crud.get_dashboard_stats(db)