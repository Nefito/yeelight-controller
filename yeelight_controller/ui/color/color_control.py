from PySide6.QtCore import Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from yeelight_controller.core.controller import (
    YeelightController,
    YeelightControllerError,
)
from yeelight_controller.core.debouncer import DebouncedAction
from yeelight_controller.ui.color.color_picker import ColorPicker


class ColorControl(QWidget):
    statusChanged = Signal(str)

    def __init__(
        self,
        controller: YeelightController,
        color: QColor,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)

        self.controller = controller
        self.current_color = color
        self.pending_color: QColor | None = None

        self.update_action = DebouncedAction(
            self.apply_pending_color,
            interval=75,
            parent=self,
        )

        self.setup_ui()
        self.update_display()

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        layout.setSpacing(10)

        self.color_picker = ColorPicker(
            self.current_color,
            self,
        )

        self.color_picker.colorChanged.connect(
            self.handle_color_change
        )

        self.color_info = QWidget()
        self.color_info.setObjectName(
            "colorInfo"
        )

        color_info_layout = QHBoxLayout(
            self.color_info
        )
        color_info_layout.setContentsMargins(
            10,
            10,
            10,
            10,
        )
        color_info_layout.setSpacing(12)

        self.color_preview = QLabel()
        self.color_preview.setObjectName(
            "colorPreview"
        )
        self.color_preview.setFixedSize(
            70,
            50,
        )

        color_values_layout = QVBoxLayout()
        color_values_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        color_values_layout.setSpacing(3)

        current_color_title = QLabel(
            "Current color"
        )
        current_color_title.setObjectName(
            "colorInfoTitle"
        )

        self.hex_label = QLabel()
        self.hex_label.setObjectName(
            "colorHex"
        )

        self.rgb_label = QLabel()
        self.rgb_label.setObjectName(
            "colorRgb"
        )

        color_values_layout.addWidget(
            current_color_title
        )
        color_values_layout.addWidget(
            self.hex_label
        )
        color_values_layout.addWidget(
            self.rgb_label
        )

        color_info_layout.addWidget(
            self.color_preview
        )
        color_info_layout.addLayout(
            color_values_layout
        )
        color_info_layout.addStretch()

        layout.addWidget(
            self.color_picker
        )
        layout.addWidget(
            self.color_info
        )

    def set_color(
        self,
        color: QColor,
    ) -> None:
        if not color.isValid():
            return

        self.current_color = color

        self.color_picker.blockSignals(
            True
        )

        self.color_picker.set_color(
            color
        )

        self.color_picker.blockSignals(
            False
        )

        self.update_display()

    def request_color(
        self,
        color: QColor,
    ) -> None:
        if not color.isValid():
            return

        if (
            color.red() == 0
            and color.green() == 0
            and color.blue() == 0
        ):
            self.statusChanged.emit(
                "● Black cannot be displayed by the lightstrip"
            )
            return

        self.pending_color = color

        self.update_display_for_pending_color(
            color
        )

        self.statusChanged.emit(
            "● Changing color..."
        )

        self.update_action.start()

    def update_display(self) -> None:
        self.update_color_information(
            self.current_color
        )

    def update_display_for_pending_color(
        self,
        color: QColor,
    ) -> None:
        self.update_color_information(
            color
        )

    def update_color_information(
        self,
        color: QColor,
    ) -> None:
        red = color.red()
        green = color.green()
        blue = color.blue()

        self.color_preview.setStyleSheet(
            f"""
            background-color: rgb(
                {red},
                {green},
                {blue}
            );
            border: 1px solid #777;
            border-radius: 6px;
            """
        )

        self.hex_label.setText(
            f"#{red:02X}{green:02X}{blue:02X}"
        )

        self.rgb_label.setText(
            f"RGB {red} · {green} · {blue}"
        )

    def handle_color_change(
        self,
        color: QColor,
    ) -> None:
        self.request_color(color)

    def apply_pending_color(self) -> None:
        if self.pending_color is None:
            return

        color = self.pending_color
        self.pending_color = None

        try:
            self.controller.set_color(
                color.red(),
                color.green(),
                color.blue(),
            )

            self.current_color = color

            self.color_picker.blockSignals(
                True
            )

            self.color_picker.set_color(
                color
            )

            self.color_picker.blockSignals(
                False
            )

            self.update_display()

            self.statusChanged.emit(
                "● On"
            )

        except YeelightControllerError as error:
            self.statusChanged.emit(
                f"● {error}"
            )