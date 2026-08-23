from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..db.database import get_db
from ..schemas import dataset, user
from ..core import security
from ..db import models
from ..core.security import get_current_user

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


@router.get("/history", response_model=list[dataset.DatasetResponse])
async def get_all_datasets(limit : int = 10, offset : int = 0, search :str = "",db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    datasets = db.query(models.dataset).join(models.Query, models.dataset.id == models.Query.dataset_id, isouter = True).filter(models.dataset.user_id == current_user.id, models.dataset.title.ilike(f"%{search}%")).limit(limit).offset(offset).all()

    if not datasets:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Datasets are not found")
    return datasets

@router.get("/dataset/{id}", response_model=dataset.DatasetResponse)
async def get_dataset(id : int, db:Session=Depends(get_db), current_user = Depends(get_current_user)):
    dataset = db.query(models.dataset).filter(models.dataset.id==id, models.dataset.user_id==current_user.id).first()

    if not dataset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"dataset is not found")
    return dataset

@router.delete("/dataset/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dataset(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    dataset = db.query(models.dataset).filter(
        models.dataset.id == id,
        models.dataset.user_id == current_user.id
    ).first()
    
    if not dataset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dataset with id {id} is not found")
    db.query(models.Query).filter(models.Query.dataset_id == id).delete()
    db.delete(dataset)
    db.commit()
    