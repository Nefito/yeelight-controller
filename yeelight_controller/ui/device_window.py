from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from yeelight_controller.core.device_manager import DeviceManager
from yeelight_controller.ui.main_window import MainWindow


class DeviceWindow(QWidget):
    """Show one independent control panel per configured lightstrip."""

    def __init__(
        self,
        device_manager: DeviceManager,
        default_device_id: str,
    ):
        super().__init__()

        self.setWindowTitle("Yeelight Controller")
        self.resize(600, 900)
        self.setMinimumSize(520, 700)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 12, 0, 0)
        layout.setSpacing(0)

        selector_layout = QHBoxLayout()
        selector_layout.setContentsMargins(24, 0, 24, 0)
        selector_layout.setSpacing(12)

        label = QLabel("Device")
        self.device_selector = QComboBox()
        self.device_selector.setObjectName("effectSelector")

        self.panels = QStackedWidget(self)

        for device in device_manager.list_devices():
            self.device_selector.addItem(device.name, device.id)
            self.panels.addWidget(
                MainWindow(
                    device_manager.get_controller(device.id),
                    device_name=device.name,
                )
            )

        selector_layout.addWidget(label)
        selector_layout.addWidget(self.device_selector, 1)
        layout.addLayout(selector_layout)
        layout.addWidget(self.panels, 1)

        self.device_selector.currentIndexChanged.connect(
            self.panels.setCurrentIndex
        )

        index = self.device_selector.findData(default_device_id)
        if index < 0:
            raise ValueError(
                f"Unknown default device: {default_device_id}"
            )

        self.device_selector.setCurrentIndex(index)
        self.panels.setCurrentIndex(index)
