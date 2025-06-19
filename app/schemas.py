from pydantic import BaseModel
from datetime import datetime

class BasicCurd(BaseModel):
    id: int
    name: str
    address: str
    human: bool =True
    created_at : datetime
    
    