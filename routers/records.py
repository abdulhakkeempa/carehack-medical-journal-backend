from fastapi import APIRouter, Depends, File, UploadFile
from typing import List
from models.model import HealthRecord, TextInput
from models.tables import health_records
from db import database
from services.data_extraction import extract_health_data

router = APIRouter()

@router.get("/get-all-records", response_model=List[HealthRecord])
async def get_all_records():
    user_id = 1
    query = health_records.select().where(health_records.c.user_id == user_id)
    rows = await database.fetch_all(query)
    return [HealthRecord(**row) for row in rows]

@router.post("/add-record/text")
async def add_record(text: TextInput):
    record = extract_health_data(text.input_date, text.text)

    if not record:
        return {"error": "Failed to extract health data from the journal entry."}

    query = health_records.insert().values(
        user_id=1,  
        date=record['date'],
        condition=record['condition'],
        type=record['type'],
        remarks=record.get('remarks', None)
    )
    last_record_id = await database.execute(query)
    return {"id": last_record_id, "record": record}

@router.post("/add-record/audio")
async def add_audio_record(file: UploadFile = File(...)):
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "message": "Audio record received successfully."
    }

@router.post("/add-record/image")
async def add_image_record(file: UploadFile = File(...)):
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "message": "Image record received successfully."
    }
