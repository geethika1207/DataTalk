from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..db.database import get_db
from ..schemas import dataset, user
from ..core import security
from ..db import models

router = APIRouter()

@router.post("/user",status_code=status.HTTP_201_CREATED, response_model=user.UserResponse)
def create_user(user_credentials:user.UserRequest, db:Session=Depends(get_db)):
    try:
        hashed_password = security.hash_password(user_credentials.password)
        user_credentials.password = hashed_password
        new_user = models.USER(**user_credentials.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")



@router.post("/login", status_code=status.HTTP_201_CREATED, response_model=dataset.LoginResponse)
def login_user(user_credentials:OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
    user_info = db.query(models.USER).filter(models.USER.email==user_credentials.username).first()
    if not user_info:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credenials")
    if not security.to_verify(user_credentials.password, user_info.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials")
    access_token = security.create_token({"user_id":user_info.id})
    return{"access_token":access_token, "token_type" : "Bearer"}