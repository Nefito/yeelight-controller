from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from yeelight_controller.core.timers.timer_manager import (
    OffTimer,
    TimerManager,
)
from yeelight_controller.ui.timers.duration_timer_control import (
    DurationTimerControl,
)
from yeelight_controller.ui.timers.scheduled_timer_control import (
    ScheduledTimerControl,
)


class TimersControl(QWidget):
    statusChanged = Signal(str)
    lightStateRefreshRequested = Signal()

    def __init__(
        self,
        timer_manager: TimerManager,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)

        self.timer_manager = timer_manager
        self.remaining_minutes: int | None = None

        self.refresh_timer = QTimer(self)
        self.refresh_timer.setInterval(10_000)
        self.refresh_timer.timeout.connect(
            self.refresh_timer_state
        )

        self.setup_ui()
        self.connect_signals()
        self.refresh_timer_state()

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        layout.setSpacing(12)

        duration_label = QLabel(
            "Turn off in"
        )
        duration_label.setObjectName(
            "timerLabel"
        )

        self.duration_control = (
            DurationTimerControl(self)
        )

        separator = QFrame(self)
        separator.setObjectName(
            "timerSeparator"
        )
        separator.setFrameShape(
            QFrame.Shape.HLine
        )

        scheduled_label = QLabel(
            "Turn off at"
        )
        scheduled_label.setObjectName(
            "timerLabel"
        )

        self.scheduled_control = (
            ScheduledTimerControl(self)
        )

        layout.addWidget(duration_label)
        layout.addWidget(
            self.duration_control
        )
        layout.addWidget(separator)
        layout.addWidget(scheduled_label)
        layout.addWidget(
            self.scheduled_control
        )

        self.create_status_controls(
            layout
        )

    def create_status_controls(
        self,
        parent_layout: QVBoxLayout,
    ) -> None:
        self.remaining_label = QLabel(
            "No timer active"
        )
        self.remaining_label.setObjectName(
            "timerRemaining"
        )

        self.cancel_button = QPushButton(
            "Cancel timer"
        )
        self.cancel_button.setObjectName(
            "timerCancelButton"
        )
        self.cancel_button.setVisible(
            False
        )

        status_layout = QHBoxLayout()
        status_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        status_layout.addWidget(
            self.remaining_label
        )
        status_layout.addStretch()
        status_layout.addWidget(
            self.cancel_button
        )

        parent_layout.addLayout(
            status_layout
        )

    def connect_signals(self) -> None:
        self.duration_control.timerRequested.connect(
            self.start_countdown
        )

        self.scheduled_control.timerRequested.connect(
            self.start_countdown
        )

        self.cancel_button.clicked.connect(
            self.timer_manager.cancel
        )

        self.timer_manager.timerStarted.connect(
            self.handle_timer_started
        )

        self.timer_manager.timerCancelled.connect(
            self.handle_timer_cancelled
        )

        self.timer_manager.errorOccurred.connect(
            self.handle_error
        )

    def start_countdown(
        self,
        minutes: int,
    ) -> None:
        if minutes <= 0:
            self.statusChanged.emit(
                "● Timer duration must be greater than zero"
            )
            return

        self.timer_manager.start_countdown(
            minutes
        )

    def refresh_timer_state(self) -> None:
        had_active_timer = (
            self.remaining_minutes is not None
        )

        timer = self.timer_manager.get_timer()

        if timer is None:
            self.show_inactive_state()

            if had_active_timer:
                self.lightStateRefreshRequested.emit()

            return

        self.show_active_state(timer)

    def show_active_state(
        self,
        timer: OffTimer,
    ) -> None:
        self.remaining_minutes = (
            timer.remaining_minutes
        )

        self.remaining_label.setText(
            self.format_remaining_time(
                self.remaining_minutes
            )
        )

        self.cancel_button.setVisible(
            True
        )

        if not self.refresh_timer.isActive():
            self.refresh_timer.start()

    def show_inactive_state(self) -> None:
        self.remaining_minutes = None

        self.remaining_label.setText(
            "No timer active"
        )

        self.cancel_button.setVisible(
            False
        )
        self.refresh_timer.stop()

    def handle_timer_started(
        self,
        minutes: int,
    ) -> None:
        timer = OffTimer(
            remaining_minutes=minutes
        )

        self.show_active_state(timer)

        self.statusChanged.emit(
            "● Turn-off timer active"
        )

    def handle_timer_cancelled(self) -> None:
        self.show_inactive_state()

        self.statusChanged.emit(
            "● Turn-off timer cancelled"
        )

    def handle_error(
        self,
        message: str,
    ) -> None:
        self.statusChanged.emit(
            f"● {message}"
        )

    def format_remaining_time(
        self,
        minutes: int,
    ) -> str:
        hours, remaining_minutes = divmod(
            minutes,
            60,
        )

        if hours == 0:
            return (
                f"Turns off in "
                f"{remaining_minutes} min"
            )

        if remaining_minutes == 0:
            return (
                f"Turns off in "
                f"{hours} h"
            )

        return (
            f"Turns off in "
            f"{hours} h "
            f"{remaining_minutes} min"
        )