from datetime import date, time
from server.schemas import DataEntryCreate, DataEntryOut


def test_01_data_entry_create_schema():

    data = {
        "date": "2023-01-01",
        "time": "12:00:00",
        "text": "Test schema",
        "click_count": 1
    }

    entry = DataEntryCreate(**data)
    assert entry.date == date(2023, 1, 1)
    assert entry.time == time(12, 0, 0)

def test_02_data_entry_out_schema():

    data = {
        "id": 1,
        "date": date(2023, 1, 1),
        "time": time(12, 0, 0),
        "text": "Test schema",
        "click_count": 1
    }

    entry = DataEntryOut(**data)
    assert entry.id == 1
