from dataclasses import dataclass
from typing import TypedDict

from PySide6.QtCore import QObject, Signal

from yeelight_controller.core.controller import (
    YeelightController,
    YeelightControllerError,
)


class YeelightTimerResponse(TypedDict):
    type: int
    delay: int
    mix: int


@dataclass
class OffTimer:
    remaining_minutes: int


class TimerManager(QObject):
    timerStarted = Signal(int)
    timerCancelled = Signal()
    errorOccurred = Signal(str)

    def __init__(
        self,
        controller: YeelightController,
        parent: QObject | None = None,
    ):
        super().__init__(parent)

        self.controller = controller

    def start_countdown(
        self,
        minutes: int,
    ) -> None:
        if minutes <= 0:
            return

        try:
            self.controller.set_off_timer(
                minutes
            )

            self.timerStarted.emit(
                minutes
            )

        except YeelightControllerError as error:
            self.errorOccurred.emit(
                str(error)
            )

    def cancel(self) -> None:
        try:
            self.controller.cancel_off_timer()
            self.timerCancelled.emit()

        except YeelightControllerError as error:
            self.errorOccurred.emit(
                str(error)
            )

    def get_timer(self) -> OffTimer | None:
        try:
            response: YeelightTimerResponse | None = (
                self.controller.get_off_timer()
            )

            if response is None:
                return None

            return OffTimer(
                remaining_minutes=response["delay"]
            )

        except YeelightControllerError as error:
            self.errorOccurred.emit(
                str(error)
            )
            return None