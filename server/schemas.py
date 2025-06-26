from pydantic import BaseModel
from datetime import date, time


class DataEntryCreate(BaseModel):
    date: date
    time: time
    text: str
    click_count: int


class DataEntryOut(DataEntryCreate):
    id: int

    class Config:
        orm_mode = True