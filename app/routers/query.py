from fastapi import APIRouter, HTTPException, Depends, status
from ..schemas import query 
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db import models
from ..core.security import get_current_user
from ..services import ai_service
import duckdb  # Add DuckDB import

router = APIRouter()

@router.post("/datasets/{id}/queries", status_code=status.HTTP_201_CREATED)
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
    
    summary_data = dataset.summary
    
    try:
        plan = ai_service.generate_query_plan(
            metadata=summary_data, 
            question=question.question,
            filepath=dataset.filepath
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="AI processing failed.")
        
    # Extract the AI's explanation and chart plan
    answer = plan.get("explanation", "Here is your analysis.")
    chart_config = plan.get("chart")
    sql_query = plan.get("sql_query")
    
    chart_data = None
    
    if sql_query:
        try:
            query_result = duckdb.query(sql_query).df()
            chart_data = query_result.to_dict(orient="records")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Database execution error: {str(e)}")
    
    final_charts_payload = {
        "config": chart_config,
        "data": chart_data
    } if (chart_config or chart_data) else None

    new_query = models.Query(
        question=question.question,
        answer=answer,
        charts=final_charts_payload,
        user_id=current_user.id,
        dataset_id=id
    )
    
    db.add(new_query)
    db.commit()
    db.refresh(new_query)
    
    return {
        "id": new_query.id, 
        "answer": answer, 
        "charts": final_charts_payload
    }