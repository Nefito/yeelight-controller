"""Start/stop controls for the Lightstrip Pro screen-sync worker."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from yeelight_controller.core.screen_sync import ScreenSyncWorker


class ScreenSyncControl(QWidget):
    runningChanged = Signal(bool)
    statusChanged = Signal(str)

    def __init__(self, strip_ip: str, parent=None):
        super().__init__(parent)
        self.strip_ip = strip_ip
        self.worker = None
        self.light_enabled = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.description = QLabel(
            "Mirror the four edges of your primary monitor at 20 FPS."
        )
        self.description.setWordWrap(True)
        self.status = QLabel("Stopped")
        self.button = QPushButton("Start Screen Sync")
        self.button.clicked.connect(self.toggle)

        layout.addWidget(self.description)
        layout.addWidget(self.status)
        layout.addWidget(self.button)

    def is_running(self) -> bool:
        return self.worker is not None

    def set_light_enabled(self, enabled: bool):
        self.light_enabled = enabled
        if not self.is_running():
            self.button.setEnabled(enabled)

    def toggle(self):
        if self.is_running():
            self.stop()
        else:
            self.start()

    def start(self):
        if self.is_running() or not self.light_enabled:
            return

        self.worker = ScreenSyncWorker(self.strip_ip, parent=self)
        self.worker.statusChanged.connect(self.status.setText)
        self.worker.syncStopped.connect(self._on_stopped)
        self.worker.finished.connect(self._on_finished)
        self.status.setText("Starting...")
        self.button.setText("Stop Screen Sync")
        self.runningChanged.emit(True)
        self.worker.start()

    def stop(self):
        if self.worker is not None:
            self.status.setText("Stopping...")
            self.button.setEnabled(False)
            self.worker.request_stop()

    def _on_stopped(self, error: str):
        if error:
            self.status.setText(f"Error: {error}")
            self.statusChanged.emit(f"● Screen sync: {error}")
        else:
            self.status.setText("Stopped")

    def _on_finished(self):
        worker = self.worker
        self.worker = None
        if worker is not None:
            worker.deleteLater()
        self.button.setText("Start Screen Sync")
        self.button.setEnabled(self.light_enabled)
        self.runningChanged.emit(False)

    def shutdown(self):
        if self.worker is not None:
            self.worker.request_stop()
            self.worker.wait(5000)
