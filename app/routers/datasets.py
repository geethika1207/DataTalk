from fastapi import APIRouter, File, UploadFile, Form, Depends, HTTPException, status
import os
import time
import shutil 
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db import models
from ..services.extract_metadata import extract_schema
from ..core.security import get_current_user
from ..schemas import dataset
from pathlib import Path

os.makedirs("uploads", exist_ok=True)
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

    if not filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    clean_filename = file.filename.replace(" ", "_")
    
    new_filename = f"{current_user.id}-{clean_filename}"

    UPLOAD_DIR = Path("uploads")

    filepath = UPLOAD_DIR / new_filename
    

    try:
        with open(filepath, "wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {e}")

        
    dataset_metadata = extract_schema(filepath)
    
    # create a new row in database
    new_dataset = models.dataset(
        filename=filename,
        filepath=str(filepath),
        title=title,
        user_id=current_user.id,
        summary=dataset_metadata
    )
    
    db.add(new_dataset)
    db.commit()
    db.refresh(new_dataset)
    
    return {
        "message": "Dataset processed successfully",
        "dataset_id": new_dataset.id
    }