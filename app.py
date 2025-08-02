from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class HealthRecord(BaseModel):
    user_id: int
    date: str
    condition: str
    type: str  # "physical" or "emotional"
    remarks: Optional[str] = None

# ----------------------------
# Dummy "database"
# ----------------------------
dummy_db: List[HealthRecord] = [
    HealthRecord(user_id=1, date="2025-08-01", condition="Felt very tired after football.", type="physical", remarks="Slept late"),
    HealthRecord(user_id=1, date="2025-08-02", condition="Felt anxious in the morning.", type="emotional"),
    HealthRecord(user_id=2, date="2025-08-01", condition="Mild knee pain during walking.", type="physical", remarks="Took painkiller"),
]

@app.get("/get-all-records", response_model=List[HealthRecord])
def get_all_records():
    return dummy_db
