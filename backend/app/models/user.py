from pydantic import BaseModel

class UserDB(BaseModel):
    id: str = None
    username:str
    password: str
    email:str
