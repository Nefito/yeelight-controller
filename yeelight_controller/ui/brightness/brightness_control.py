from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from yeelight_controller.core.controller import (
    YeelightController,
    YeelightControllerError,
)
from yeelight_controller.core.debouncer import DebouncedAction


class BrightnessControl(QWidget):
    statusChanged = Signal(str)

    def __init__(
        self,
        controller: YeelightController,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)

        self.controller = controller
        self.current_brightness = 100
        self.pending_brightness: int | None = None

        self.update_action = DebouncedAction(
            self.apply_pending_brightness,
            interval=75,
            parent=self,
        )

        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        layout.setSpacing(8)

        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        title = QLabel("Brightness")
        title.setObjectName(
            "brightnessTitle"
        )

        self.value_label = QLabel(
            "100%"
        )
        self.value_label.setObjectName(
            "brightnessValue"
        )

        title_layout.addWidget(title)
        title_layout.addStretch()
        title_layout.addWidget(
            self.value_label
        )

        self.slider = QSlider(
            Qt.Orientation.Horizontal
        )
        self.slider.setRange(
            1,
            100,
        )
        self.slider.setValue(
            self.current_brightness
        )
        self.slider.setMinimumHeight(
            24
        )

        self.slider.valueChanged.connect(
            self.handle_brightness_change
        )

        layout.addLayout(
            title_layout
        )
        layout.addWidget(
            self.slider
        )

    def set_brightness(
        self,
        brightness: int,
    ) -> None:
        brightness = max(
            1,
            min(
                100,
                brightness,
            ),
        )

        self.current_brightness = brightness

        self.slider.blockSignals(
            True
        )

        self.slider.setValue(
            brightness
        )

        self.slider.blockSignals(
            False
        )

        self.update_display()

    def handle_brightness_change(
        self,
        brightness: int,
    ) -> None:
        self.current_brightness = brightness
        self.value_label.setText(
            f"{brightness}%"
        )

        self.pending_brightness = brightness

        self.statusChanged.emit(
            "● Changing brightness..."
        )

        self.update_action.start()

    def apply_pending_brightness(self) -> None:
        if self.pending_brightness is None:
            return

        brightness = self.pending_brightness
        self.pending_brightness = None

        try:
            self.controller.set_brightness(
                brightness
            )

            self.current_brightness = brightness

            self.update_display()

            self.statusChanged.emit(
                "● On"
            )

        except YeelightControllerError as error:
            self.statusChanged.emit(
                f"● {error}"
            )

    def update_display(self) -> None:
        self.value_label.setText(
            f"{self.current_brightness}%"
        )