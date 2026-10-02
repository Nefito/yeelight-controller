import sys

from PySide6.QtWidgets import QApplication

from config import YEELIGHT_IP
from yeelight_controller.core.controller import YeelightController
from yeelight_controller.ui.main_window import MainWindow
from yeelight_controller.ui.styles import APP_STYLE


def main() -> None:
    app = QApplication(sys.argv)

    app.setStyleSheet(APP_STYLE)

    controller = YeelightController(YEELIGHT_IP)
    window = MainWindow(controller)

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()