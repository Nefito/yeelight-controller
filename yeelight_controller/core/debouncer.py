from collections.abc import Callable

from PySide6.QtCore import QObject, QTimer


class DebouncedAction(QObject):
    def __init__(
        self,
        callback: Callable[[], None],
        interval: int = 75,
        parent: QObject | None = None,
    ):
        super().__init__(parent)

        self.callback = callback

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.setInterval(interval)
        self.timer.timeout.connect(self.execute)

    def start(self) -> None:
        self.timer.start()

    def cancel(self) -> None:
        self.timer.stop()

    def execute(self) -> None:
        self.callback()