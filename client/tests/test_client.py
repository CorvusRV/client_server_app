import pytest
from unittest.mock import patch, MagicMock
from client.app import ClientApp
from client.config import Config


@pytest.fixture
def client_app(qtbot):
    """Фикстура для создания тестового экземпляра приложения"""
    window = ClientApp()
    window._mock_message_handler = MagicMock()  # Мокируем обработчик сообщений
    qtbot.addWidget(window)
    yield window
    window.close()

def test_01_send_data_success(client_app):
    """Тест успешной отправки данных"""

    test_text = "Test message"
    client_app.input_line.setText(test_text)

    with patch('client.app.requests.post') as mock_post:
        mock_post.return_value = MagicMock(status_code=200)
        client_app.send_data()

        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert kwargs['json']['text'] == test_text
        assert kwargs['json']['click_count'] == 1

        client_app._mock_message_handler.assert_called_once_with(
            "Успех", "Данные успешно отправлены!", 'info'
        )

def test_02_send_data_empty_input(client_app):
    """Тест отправки с пустым вводом"""

    client_app.input_line.clear()
    client_app.send_data()

    client_app._mock_message_handler.assert_called_once_with(
        "Предупреждение", "Введите текст!", 'warning'
    )

    assert client_app.click_count == 0

def test_03_send_data_failure(client_app):
    """Тест обработки ошибки"""

    client_app.input_line.setText("Test")

    with patch('client.app.requests.post') as mock_post:
        mock_post.side_effect = Exception("error")
        client_app.send_data()

        client_app._mock_message_handler.assert_called_once_with(
            "Ошибка", "Не удалось отправить данные: error", 'error'
        )

def test_04_getting_data_success(client_app):
    """Тест успешного получения данных"""

    test_data = [{
        "date": "2023-01-01",
        "time": "12:00:00",
        "text": "Test item",
        "click_count": 1,
        "id": 1
    }]

    with patch('client.app.requests.get') as mock_get:
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: test_data
        )
        client_app.getting_data()

        assert client_app.list_model.stringList() == [
            "2023-01-01 12:00:00 | Test item | Click: 1"
        ]

        mock_get.assert_called_once_with(
            client_app.get_server_url(Config.S_GET_ENDPOINT)
        )
