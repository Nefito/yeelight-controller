from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QAbstractSpinBox,
    QHBoxLayout,
    QPushButton,
    QSpinBox,
    QWidget,
)

from yeelight_controller.ui.timers.arrow_stepper import (
    SteppedInput,
)


class DurationTimerControl(QWidget):
    timerRequested = Signal(int)

    def __init__(
        self,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)

        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        layout.setSpacing(8)

        self.hours_input = QSpinBox()
        self.hours_input.setObjectName(
            "timerInput"
        )
        self.hours_input.setRange(0, 23)
        self.hours_input.setValue(1)
        self.hours_input.setSuffix(" h")
        self.hours_input.setButtonSymbols(
            QAbstractSpinBox.ButtonSymbols.NoButtons
        )

        hours_input = SteppedInput(
            self.hours_input,
            self.hours_input.stepUp,
            self.hours_input.stepDown,
            self,
        )

        self.minutes_input = QSpinBox()
        self.minutes_input.setObjectName(
            "timerInput"
        )
        self.minutes_input.setRange(0, 59)
        self.minutes_input.setValue(0)
        self.minutes_input.setSuffix(
            " min"
        )
        self.minutes_input.setButtonSymbols(
            QAbstractSpinBox.ButtonSymbols.NoButtons
        )

        minutes_input = SteppedInput(
            self.minutes_input,
            self.minutes_input.stepUp,
            self.minutes_input.stepDown,
            self,
        )

        start_button = QPushButton(
            "Start timer"
        )
        start_button.setObjectName(
            "timerButton"
        )
        start_button.clicked.connect(
            self.request_timer
        )

        layout.addWidget(hours_input)
        layout.addWidget(minutes_input)
        layout.addStretch()
        layout.addWidget(start_button)

    def request_timer(self) -> None:
        total_minutes = (
            self.hours_input.value() * 60
            + self.minutes_input.value()
        )

        self.timerRequested.emit(
            total_minutes
        )