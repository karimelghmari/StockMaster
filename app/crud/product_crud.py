from sqlalchemy.orm import Session
from .. import models,schemas
def create_product(db:Session,product:schemas.ProductCreate):
    db_product=models.Product(
        name=product.name,
        price=product.price,
        description=product.description,
        quantity=product.quantity,
        min_stock_level=product.min_stock_level   
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db:Session,skip:int=0,limit:int=100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def get_product(db:Session,product_id:int):
    return db.query(models.Product).filter(models.Product.id==product_id).first()

def update_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    db_product = get_product(db, product_id)
    if not db_product:
        return None
    update_data = product.model_dump(exclude_unset=True) 
    for key, value in update_data.items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session,product_id:int):
    old_product=get_product(db,product_id)
    if not old_product:
        return None
    db.delete(old_product)
    db.commit()
    return True

def get_dashboard_stats(db: Session):
    products = db.query(models.Product).all()
    total_value = sum(p.price * p.quantity for p in products)
    total_trans = db.query(models.Transaction).count()

    low_stock_items = db.query(models.Product).filter(
        models.Product.quantity <= models.Product.min_stock_level
    ).all()
    
    return {
        "total_products": len(products),
        "total_inventory_value": total_value,
        "low_stock_count": len(low_stock_items),
        "total_transactions": total_trans,
        "low_stock_items": low_stock_items
    }
        