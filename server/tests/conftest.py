import pytest
from sqlalchemy import create_engine
from server.config import Config
from server.database import Base, Database


@pytest.fixture(scope="session")
def test_db_engine():
    """Фикстура для тестового движка БД"""
    engine = create_engine(f"{Config.DB_URL}_test", echo=Config.DB_ECHO)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def database(monkeypatch):
    """Фикстура для Database с тестовой конфигурацией"""
    # Временная конфигурация
    test_db_url = f"{Config.DB_URL}_test"

    # Подменяем конфигурацию
    monkeypatch.setattr(Config, 'DB_URL', test_db_url)
    monkeypatch.setattr(Config, 'DB_ECHO', False)

    # Создаем Database
    return Database()


@pytest.fixture
def server_app(database):
    """Фикстура для ServerApp"""
    from server.app import ServerApp
    return ServerApp(database)


@pytest.fixture
def client(server_app):
    """Тестовый клиент"""
    from fastapi.testclient import TestClient
    return TestClient(server_app.app, base_url="http://testserver")
