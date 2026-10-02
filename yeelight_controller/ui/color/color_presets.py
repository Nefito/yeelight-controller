from typing import ClassVar

from PySide6.QtCore import Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QGridLayout,
    QPushButton,
    QWidget,
)


class ColorPresets(QWidget):
    colorSelected = Signal(QColor)

    PRESETS: ClassVar[list[tuple[str, QColor]]] = [
        ("Red", QColor(255, 0, 0)),
        ("Orange", QColor(255, 128, 0)),
        ("Yellow", QColor(255, 255, 0)),
        ("Green", QColor(0, 255, 0)),
        ("Cyan", QColor(0, 255, 255)),
        ("Blue", QColor(0, 0, 255)),
        ("Purple", QColor(128, 0, 255)),
        ("White", QColor(255, 255, 255)),
    ]

    def __init__(
        self,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)

        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setHorizontalSpacing(8)
        layout.setVerticalSpacing(8)

        for index, (name, color) in enumerate(
            self.PRESETS
        ):
            preset = self.create_preset(
                name,
                color,
            )

            row = index // 4
            column = index % 4

            layout.addWidget(
                preset,
                row,
                column,
            )

    def create_preset(
        self,
        name: str,
        color: QColor,
    ) -> QPushButton:
        button = QPushButton(name)

        button.setObjectName("presetButton")
        button.setMinimumHeight(54)

        red = color.red()
        green = color.green()
        blue = color.blue()

        text_color = self.get_text_color(
            color
        )

        button.setStyleSheet(
            f"""
            QPushButton#presetButton {{
                background-color: rgb(
                    {red},
                    {green},
                    {blue}
                );
                color: {text_color};
                border: 1px solid rgba(
                    255,
                    255,
                    255,
                    90
                );
                border-radius: 7px;
                font-weight: 600;
            }}

            QPushButton#presetButton:hover {{
                border: 2px solid #ffffff;
            }}

            QPushButton#presetButton:pressed {{
                border: 2px solid #8ab4f8;
            }}

            QPushButton#presetButton:disabled {{
                border: 1px solid rgba(
                    255,
                    255,
                    255,
                    90
                );
            }}
            """
        )

        button.clicked.connect(
            lambda: self.colorSelected.emit(color)
        )

        return button

    @staticmethod
    def get_text_color(color: QColor) -> str:
        luminance = (
            0.299 * color.red()
            + 0.587 * color.green()
            + 0.114 * color.blue()
        )

        if luminance > 160:
            return "#202124"

        return "#ffffff"
