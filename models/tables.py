from sqlalchemy import Table, Column, Integer, String, Date
from sqlalchemy.sql import text
from db import metadata

health_records = Table(
    "health_records",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, nullable=False),
    Column("date", String, nullable=False),
    Column("condition", String, nullable=False),
    Column("type", String, nullable=False),
    Column("remarks", String, nullable=True),
    Column("source", String, nullable=True),  # Added source column
    Column("created_at", Date, nullable=False, server_default=text('CURRENT_DATE'))
)
