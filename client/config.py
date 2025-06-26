class Config:
    """Класс для хранения конфигурации приложения"""

    # Параметры сервера
    S_HOST = "http://localhost"
    S_PORT = 8000
    S_POST_ENDPOINT = "/data"
    S_GET_ENDPOINT = "/data"

    # Параметры настройки клиента
    C_WIDTH = 400
    C_HEIGHT = 400

    @classmethod
    def get_server_url(cls, endpoint: str) -> str:
        """Сформировать URL сервера"""
        return f"{cls.S_HOST}:{cls.S_PORT}{endpoint}"
