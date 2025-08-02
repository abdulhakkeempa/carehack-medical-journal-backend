from typing import Optional
from pydantic import BaseModel

class HealthRecord(BaseModel):
    user_id: int
    date: str
    condition: str
    type: str  
    remarks: Optional[str] = None


class TextInput(BaseModel):
    input_date: str
    text: str
