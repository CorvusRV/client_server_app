from sqlalchemy import inspect
from server.config import Config


def test_database_creation(database):
    """Тест инициализации Database"""
    assert database.engine is not None
    assert database.SessionLocal is not None
    assert str(database.engine.url) == Config.TEST_DB_URL


def test_get_db(database):
    """Тест получения сессии БД"""
    gen = database.get_db()
    db = next(gen)
    try:
        assert db.is_active
    finally:
        try:
            next(gen)  # Завершаем генератор
        except StopIteration:
            pass


def test_create_tables(database):
    """Тест создания таблиц"""
    from server.models import DataEntry
    database.create_tables()

    # Проверяем, что таблица существует
    inspector = inspect(database.engine)
    assert "data_entries" in inspector.get_table_names()