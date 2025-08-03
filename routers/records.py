from fastapi import APIRouter, Depends, File, UploadFile
from typing import List
from models.model import HealthRecord, TextInput
from models.tables import health_records
from db import database
from services.data_extraction import extract_health_data
from services.ocr import OCR
from services.stt import whisper_transcribe
from datetime import datetime
import wave
import librosa
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
        source="text",
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

    ocr_result = await OCR(contents)

    if not ocr_result:
        return {"error": "Failed to extract text from the image."}

    input_date = datetime.now().strftime("%Y-%m-%d")

    record = extract_health_data(input_date, ocr_result)

    query = health_records.insert().values(
        user_id=1,  
        date=record['date'],
        condition=record['condition'],
        type=record['type'],
        source="image",
        remarks=record.get('remarks', None)
    )

    last_record_id = await database.execute(query)
    return {"id": last_record_id, "record": record}

def read_wave_file(uploaded_file: UploadFile) -> dict:
    with wave.open(uploaded_file.file, 'rb') as wave_file:
        params = wave_file.getparams()
        frames = wave_file.readframes(params.nframes)
        duration = params.nframes / params.framerate
        return {
            "channels": params.nchannels,
            "sample_width": params.sampwidth,
            "frame_rate": params.framerate,
            "num_frames": params.nframes,
            "duration": duration,
            "frames": frames
        }    
    
@router.post("/add-record/audio/transcribe")
async def transcribe(file: UploadFile = File(...)):
    # content = await file.read()
    content = await file.read()
    print("audio file type (before): ", content[0:20])
    audio,_ = librosa.load(content)#.decode('utf-8')
    # audio = base64.b64encode(content).decode('utf-8')
    # contents = await file.read()
    # print("\n\n audio file type(after): ", type(audio))
    # print("audio file shape: ", audio[0:20])
    transcribtion_result = await whisper_transcribe(audio)

    if not transcribtion_result:
        return {"error": "Failed to extract the transcription from the audio."}

    return {
        "transcription": transcribtion_result
    }
