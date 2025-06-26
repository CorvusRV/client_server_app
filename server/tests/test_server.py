from fastapi import status
from sqlalchemy import inspect
from server.config import Config


def test_01_server_app_initialization(server_app):
    """Тест инициализации ServerApp"""
    assert server_app.app.title == "Сервер"
    assert len(server_app.app.routes) > 0
    assert any(middleware.cls.__name__ == "CORSMiddleware"
               for middleware in server_app.app.user_middleware)


def test_02_create_data_entry(client):
    """Тест создания записи"""
    test_data = {
        "date": "2025-01-01",  # Фиксированная дата для стабильности теста
        "time": "12:00:00",
        "text": "Тестовые данные",
        "click_count": 1
    }

    response = client.post("/data/", json=test_data)
    assert response.status_code == 200
    result = response.json()
    assert result["text"] == "Тестовые данные"
    assert "id" in result


def test_03_startup_event_creates_tables(server_app, database):
    """Тест создания таблиц при старте"""

    inspector = inspect(database.engine)
    assert "data_entries" in inspector.get_table_names()


def test_04_invalid_data_format(client):
    """Тест обработки невалидных данных"""
    response = client.post(Config.S_POST_ENDPOINT, json={
        "date": "invalid-date",
        "time": "12:00:00",
        "text": "Test",
        "click_count": 1
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

