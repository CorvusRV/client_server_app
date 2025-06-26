from sqlalchemy import Column, Integer, String, Date, Time
from server.database import Base


class DataEntry(Base):
    __tablename__ = "data_entries"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    time = Column(Time)
    text = Column(String, index=True)
    click_count = Column(Integer)
