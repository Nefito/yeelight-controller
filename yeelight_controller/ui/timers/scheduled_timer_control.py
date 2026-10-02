import math
from datetime import datetime, timedelta

from PySide6.QtCore import QTime, Signal
from PySide6.QtWidgets import (
    QAbstractSpinBox,
    QHBoxLayout,
    QPushButton,
    QTimeEdit,
    QWidget,
)

from yeelight_controller.ui.timers.arrow_stepper import (
    SteppedInput,
)


class ScheduledTimerControl(QWidget):
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

        self.time_input = QTimeEdit()
        self.time_input.setObjectName(
            "timerTimeInput"
        )
        self.time_input.setDisplayFormat(
            "HH:mm"
        )
        self.time_input.setWrapping(True)
        self.time_input.setTime(
            self.default_off_time()
        )
        self.time_input.setButtonSymbols(
            QAbstractSpinBox.ButtonSymbols.NoButtons
        )

        time_input = SteppedInput(
            self.time_input,
            self.time_input.stepUp,
            self.time_input.stepDown,
            self,
        )

        set_time_button = QPushButton(
            "Set time"
        )
        set_time_button.setObjectName(
            "timerButton"
        )
        set_time_button.clicked.connect(
            self.request_timer
        )

        layout.addWidget(time_input)
        layout.addStretch()
        layout.addWidget(set_time_button)

    def request_timer(self) -> None:
        self.timerRequested.emit(
            self.minutes_until_selected_time()
        )

    def minutes_until_selected_time(
        self,
    ) -> int:
        now = self.local_now()

        selected_time = self.time_input.time()

        target = now.replace(
            hour=selected_time.hour(),
            minute=selected_time.minute(),
            second=0,
            microsecond=0,
        )

        if target <= now:
            target += timedelta(days=1)

        seconds_until_target = (
            target - now
        ).total_seconds()

        return math.ceil(
            seconds_until_target / 60
        )

    def default_off_time(self) -> QTime:
        default_target = (
            self.local_now()
            + timedelta(minutes=10)
        )

        return QTime(
            default_target.hour,
            default_target.minute,
        )

    def local_now(self) -> datetime:
        local_timezone = (
            datetime.now()
            .astimezone()
            .tzinfo
        )

        return datetime.now(
            tz=local_timezone
        )