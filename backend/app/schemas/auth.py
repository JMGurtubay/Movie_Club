from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict



class AuthRequest(BaseModel):
    username:str
    password:str

class AuthResponse(BaseModel):
    code: int
    message: str
    description: str
    data: Optional[Dict] = None