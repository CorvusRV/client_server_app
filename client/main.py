import sys
from PySide6.QtWidgets import QApplication

from client.app import ClientApp


def main():
    app = QApplication(sys.argv)
    window = ClientApp()
    window.show()
    sys.exit(app.exec())
