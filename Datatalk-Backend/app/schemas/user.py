from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserRequest(BaseModel):
    email : EmailStr
    password : str

class UserResponse(BaseModel):
    id : int
    email : EmailStr
    class Config():
        orm_mode = True