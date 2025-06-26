import requests
from datetime import datetime
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLineEdit, QListView, QPushButton, QMessageBox
from PySide6.QtCore import QStringListModel

from client.config import Config


class ClientApp(QMainWindow):
    """Приложение клиента"""

    def __init__(self):
        super().__init__()
        self.click_count = 0
        self.host = Config.S_HOST
        self.port = Config.S_PORT
        self.init_ui(Config.C_WIDTH, Config.C_HEIGHT)
        self.send_button.clicked.connect(self.send_data)
        self.getting_button.clicked.connect(self.getting_data)

    def show_message(self, title: str, message: str, message_type: str = 'info'):
        """Показ сообщения с возможностью переопределения в тестах"""
        if hasattr(self, '_mock_message_handler'):
            self._mock_message_handler(title, message, message_type)
            return

        if message_type == 'info':
            QMessageBox.information(self, title, message)
        elif message_type == 'warning':
            QMessageBox.warning(self, title, message)
        elif message_type == 'error':
            QMessageBox.critical(self, title, message)

    def get_server_url(self, endpoint: str) -> str:
        """Получение адреса сервера"""

        return f"{self.host}:{self.port}{endpoint}"

    def init_ui(self, width: int, height: int):
        """Инициализация UI клиента"""

        self.setWindowTitle("Клиент")
        self.setGeometry(100,
                         100,
                         width,
                         height)
        layout = QVBoxLayout()

        self.input_line = QLineEdit(self)
        self.input_line.setPlaceholderText("Введите текст...")
        layout.addWidget(self.input_line)

        self.send_button = QPushButton("Отправить данные", self)
        self.send_button.clicked.connect(self.send_data)
        layout.addWidget(self.send_button)

        self.getting_button = QPushButton("Получить данные", self)
        self.getting_button.clicked.connect(self.getting_data)
        layout.addWidget(self.getting_button)

        self.list_view = QListView(self)
        self.list_model = QStringListModel()
        self.list_view.setModel(self.list_model)
        layout.addWidget(self.list_view)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def send_data(self):
        """Отправка данные"""

        text = self.input_line.text()
        if not text:
            self.show_message("Предупреждение", "Введите текст!", "warning")
            return

        self.click_count += 1
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")

        data = {
            "date": current_date,
            "time": current_time,
            "text": text,
            "click_count": self.click_count
        }

        try:
            url = self.get_server_url(Config.S_POST_ENDPOINT)
            response = requests.post(url, json=data)
            response.raise_for_status()
            self.show_message("Успех", "Данные успешно отправлены!")
        except Exception as e:
            self.show_message("Ошибка", f"Не удалось отправить данные: {str(e)}", 'error')

    def getting_data(self):
        """Получение данных"""

        try:
            url = self.get_server_url(Config.S_GET_ENDPOINT)
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            if isinstance(data, list):
                items = [
                    f"{item.get('date', '')} {item.get('time', '')} | {item.get('text', '')} | Click: {item.get('click_count', 0)}"
                    for item in data]
                self.list_model.setStringList(items)
        except Exception as e:
            self.show_message("Ошибка", f"Не удалось получить данные: {str(e)}", 'error')
