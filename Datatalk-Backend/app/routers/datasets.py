from fastapi import APIRouter, File, UploadFile, Form, Depends, HTTPException, status
import os
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db import models
from ..services.csv_service import create_summary
from ..core.security import get_current_user
from ..schemas import dataset

os.makedirs("uploads",exist_ok=True)
router = APIRouter(tags=["Upload Files"])
@router.post("/datasets/upload", status_code=status.HTTP_201_CREATED)
async def upload_dataset(
    file: UploadFile = File(...),
    title: str = Form(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # get filename
    filename = file.filename

    # Check 
    if not filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    # Unique filepath
    filepath = f"uploads/{current_user.id}-{filename}"
    
    # save actual file into folder
    with open(filepath, "wb") as f:
        content = await file.read()
        f.write(content)
    summary = create_summary(filepath)
    
    # create a new row in database
    new_dataset = models.dataset(
        filename=filename,
        filepath=filepath,
        title=title,
        user_id=current_user.id,
        summary=summary
    )
    
    db.add(new_dataset)
    db.commit()
    db.refresh(new_dataset)
    
    return {"message": "dataset successfully created", "id": new_dataset.id}

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
    