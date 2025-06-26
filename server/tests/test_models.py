from datetime import date, time
from server.models import DataEntry


def test_01_data_entry_model(db_session):

    entry = DataEntry(
        date=date(2023, 1, 1),
        time=time(12, 0, 0),
        text="Test model",
        click_count=1
    )

    db_session.add(entry)
    db_session.commit()

    assert entry.id is not None
    assert entry.text == "Test model"
    assert str(entry.date) == "2023-01-01"
