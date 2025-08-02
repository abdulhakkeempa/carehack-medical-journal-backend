from fastapi import FastAPI
from typing import List
from models.model import HealthRecord, TextInput
from fastapi import File, UploadFile
from services.data_extraction import extract_health_data

app = FastAPI()

dummy_db: List[HealthRecord] = [
    HealthRecord(user_id=1, date="2025-08-01", condition="Felt very tired after football.", type="physical", remarks="Slept late"),
    HealthRecord(user_id=1, date="2025-08-02", condition="Felt anxious in the morning.", type="emotional"),
    HealthRecord(user_id=1, date="2025-08-01", condition="Mild knee pain during walking.", type="physical", remarks="Took painkiller"),
]

@app.get("/get-all-records", response_model=List[HealthRecord])
def get_all_records():
    return dummy_db


@app.post("/add-record/text")
def add_record(text: TextInput):
    record = extract_health_data(text.text)
    return record



@app.post("/add-record/audio")
async def add_audio_record(file: UploadFile = File(...)):
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "message": "Audio record received successfully."
    }


@app.post("/add-record/image")
async def add_image_record(file: UploadFile = File(...)):
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "message": "Image record received successfully."
    }
