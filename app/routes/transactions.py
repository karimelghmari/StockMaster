from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas,models
from typing import List
from ..database import get_db
from ..crud import transaction_crud
from .auth import get_current_user

router=APIRouter(prefix="/transactions",tags=["Transactions"])

#create transaction
@router.post("/",response_model=schemas.Transaction)
def create_transaction(transaction:schemas.TransactionCreate,db:Session=Depends(get_db),current_user: models.User = Depends(get_current_user)):
    return transaction_crud.create_transaction(db,transaction)

#read transactions
@router.get("/",response_model=List[schemas.Transaction])
def read_transaction(db:Session=Depends(get_db),product_id:int=None,skip:int=0,limit:int=100):
    query = db.query(models.Transaction)
    # Si on a un product_id, on ajoute un filtre à la requête
    if product_id:
        query = query.filter(models.Transaction.product_id == product_id)
    return query.offset(skip).limit(limit).all()
