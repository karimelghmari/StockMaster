from sqlalchemy.orm import Session
from .. import models,schemas
from fastapi import HTTPException

def create_transaction(db:Session,transaction:schemas.TransactionCreate):
    db_transaction=models.Transaction(**transaction.model_dump())# model_dump() is the Pydantic v2 replacement for the deprecated dict() method
    db.add(db_transaction)
    product=db.query(models.Product).filter(models.Product.id==transaction.product_id).first()
    if product:
        if transaction.type==schemas.TransactionType.sale:
            if transaction.quantity>product.quantity:
                raise HTTPException(status_code=400,detail="Not enough in stock")
            else:
                product.quantity-=transaction.quantity
        elif transaction.type==schemas.TransactionType.restock:
            product.quantity+=transaction.quantity
    else:
        raise HTTPException(status_code=404,detail="item not found")
    db.commit()
    db.refresh(db_transaction)
    return db_transaction