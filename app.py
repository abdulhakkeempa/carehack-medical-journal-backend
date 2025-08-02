

from fastapi import FastAPI
from db import database, engine
from models.tables import health_records
from routers import records, chat
from db import metadata

app = FastAPI()

@app.on_event("startup")
async def startup():
    # Create tables if they do not exist
    metadata.create_all(engine)
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(records.router)
app.include_router(chat.router)
