from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..db.database import get_db
from ..schemas import dataset, user
from ..core import security
from ..db import models

router = APIRouter()

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
    