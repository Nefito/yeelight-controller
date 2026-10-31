import sys

from PySide6.QtWidgets import QApplication

from config import DEFAULT_DEVICE_ID, YEELIGHT_DEVICES
from yeelight_controller.core.device_manager import DeviceManager
from yeelight_controller.ui.device_window import DeviceWindow
from yeelight_controller.ui.styles import APP_STYLE


def main() -> None:
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)

    device_manager = DeviceManager(YEELIGHT_DEVICES)
    window = DeviceWindow(device_manager, DEFAULT_DEVICE_ID)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
