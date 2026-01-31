from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas
from ..crud import user_crud
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from ..security import verify_password, create_access_token,SECRET_KEY,ALGORITHM
from jose import JWTError, jwt

router=APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/register",response_model=schemas.UserOut)
def register_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    db_user=user_crud.get_user_by_username(db,username=user.username)
    if db_user:
        raise HTTPException(status_code=400,detail="user already exist")
    return user_crud.create_user(db,user=user)

@router.post("/login",response_model=schemas.Token)
def login(db:Session=Depends(get_db),form_data:OAuth2PasswordRequestForm=Depends()):
    user=user_crud.get_user_by_username(db,form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401,detail="username or password incorrect",headers={"WWW-Authenticate": "Bearer"})
    access_token=create_access_token(data={"sub":user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Indique à FastAPI où aller chercher le Token (sur la route /auth/login)
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="auth/login")
def get_current_user(db:Session=Depends(get_db),token:str=Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str=payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user=user_crud.get_user_by_username(db,username=username)
    if user is None:
        raise credentials_exception
    return user
    