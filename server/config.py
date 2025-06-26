class Config:
    """Класс для хранения конфигурации сервера"""
    # Базовые параметры настройки сервера
    S_HOST = "0.0.0.0"
    S_PORT = 8000
    S_POST_ENDPOINT = "/data/"
    S_GET_ENDPOINT = "/data/"

    # Базовые параметры настройки БД
    DB_URL = "sqlite:///./data.db"
    DB_ECHO = False

    # URL тестовой БД
    TEST_DB_URL = f"{DB_URL}_test"