from fastapi import APIRouter, HTTPException, Depends,status
from ..schemas import query 
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db import models
from ..core.security import get_current_user
from ..services import ai_service, csv_service
router = APIRouter()
@router.post("/datasets/{id}/queries",status_code = status.HTTP_201_CREATED)
async def create_query(
    id: int,
    question: query.QueryRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    dataset = db.query(models.dataset).filter(
        models.dataset.id == id,
        models.dataset.user_id == current_user.id
    ).first()
    
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    filepath = dataset.filepath
    summary_data = csv_service.create_summary(filepath)
    prompt = ai_service.create_prompt(summary_data, question.question)
    answer, charts = ai_service.ask_gemini(prompt)
    
    new_query = models.Query(
        question = question.question,
        answer = answer,
        charts = charts,
        user_id = current_user.id,
        dataset_id = id
    )
    
    db.add(new_query)
    db.commit()
    db.refresh(new_query)
    return {"id": new_query.id, "answer": answer, "charts": charts}
