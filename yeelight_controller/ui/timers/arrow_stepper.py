from collections.abc import Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QToolButton,
    QVBoxLayout,
    QWidget,
)


class ArrowStepper(QWidget):
    def __init__(
        self,
        step_up: Callable[[], None],
        step_down: Callable[[], None],
        parent: QWidget | None = None,
    ):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        layout.setSpacing(1)

        up_button = QToolButton(self)
        up_button.setObjectName(
            "timerArrowButton"
        )
        up_button.setArrowType(
            Qt.ArrowType.UpArrow
        )
        up_button.setAutoRaise(True)
        up_button.clicked.connect(
            step_up
        )

        down_button = QToolButton(self)
        down_button.setObjectName(
            "timerArrowButton"
        )
        down_button.setArrowType(
            Qt.ArrowType.DownArrow
        )
        down_button.setAutoRaise(True)
        down_button.clicked.connect(
            step_down
        )

        layout.addWidget(up_button)
        layout.addWidget(down_button)


class SteppedInput(QWidget):
    def __init__(
        self,
        input_widget: QWidget,
        step_up: Callable[[], None],
        step_down: Callable[[], None],
        parent: QWidget | None = None,
    ):
        super().__init__(parent)

        self.setObjectName(
            "timerInputContainer"
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        layout.setSpacing(2)

        stepper = ArrowStepper(
            step_up,
            step_down,
            self,
        )

        layout.addWidget(input_widget)
        layout.addWidget(stepper)