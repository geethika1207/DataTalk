from pydantic import BaseModel
from typing import Optional
class LoginResponse(BaseModel):
    access_token : str
    token_type : str

class QueryResponse(BaseModel):
    id : int
    question : str
    answer : str
    charts : Optional[dict] = None
    class Config:
        orm_mode = True

class DatasetResponse(BaseModel):
    id : int
    title : str
    filename : str
    queries : list[QueryResponse] = []
    class Config:
        orm_mode = True