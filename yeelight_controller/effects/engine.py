from PySide6.QtCore import QObject, Signal

from yeelight_controller.core.controller import (
    YeelightController,
    YeelightControllerError,
)
from yeelight_controller.effects.base import Effect


class EffectEngine(QObject):
    errorOccurred = Signal(str)
    runningChanged = Signal(bool)

    def __init__(
        self,
        controller: YeelightController,
        parent: QObject | None = None,
    ):
        super().__init__(parent)

        self.controller = controller
        self.effect: Effect | None = None
        self.running = False
        self.speed = 1.0

    def start(
        self,
        effect: Effect,
    ) -> None:
        try:
            if effect.supports_speed:
                speed = self.speed
            else:
                speed = effect.default_speed

            flow = effect.create_flow(speed)

            self.controller.start_flow(flow)

            self.effect = effect
            self.running = True

            self.runningChanged.emit(True)

        except YeelightControllerError as error:
            self.errorOccurred.emit(
                str(error)
            )

    def stop(self) -> None:
        if not self.running:
            return

        try:
            self.controller.stop_flow()

            self.effect = None
            self.running = False

            self.runningChanged.emit(False)

        except YeelightControllerError as error:
            self.errorOccurred.emit(
                str(error)
            )

    def sync_running_state(
        self,
        running: bool,
    ) -> None:
        self.running = running

        if not running:
            self.effect = None

        self.runningChanged.emit(running)

    def set_speed(
        self,
        speed: float,
    ) -> None:
        self.speed = speed

        if not self.running:
            return

        if self.effect is None:
            return

        if not self.effect.supports_speed:
            return

        try:
            flow = self.effect.create_flow(
                self.speed
            )

            self.controller.start_flow(flow)

        except YeelightControllerError as error:
            self.errorOccurred.emit(
                str(error)
            )

    def is_running(self) -> bool:
        return self.running