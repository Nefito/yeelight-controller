from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from yeelight_controller.core.controller import (
    YeelightController,
    YeelightControllerError,
)
from yeelight_controller.core.timers.timer_manager import TimerManager
from yeelight_controller.effects.engine import EffectEngine
from yeelight_controller.ui.control_panel import (
    ControlPanel,
)


class MainWindow(QWidget):
    def __init__(
        self,
        controller: YeelightController,
    ):
        super().__init__()

        self.controller = controller
        self.is_light_on = False
        self.effect_is_running = False

        self.effect_engine = EffectEngine(
            controller,
            self,
        )

        self.timer_manager = TimerManager(
            controller,
            self,
        )

        self.setup_ui()
        self.load_initial_state()

    def setup_ui(self) -> None:
        self.setWindowTitle(
            "Yeelight Controller"
        )
        self.resize(600, 850)
        self.setMinimumSize(
            520,
            650,
        )

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(
            20,
            18,
            20,
            20,
        )
        self.layout.setSpacing(12)

        self.create_header()

        self.control_panel = ControlPanel(
            self.controller,
            self.effect_engine,
            self.timer_manager,
            self,
        )

        self.control_panel.statusChanged.connect(
            self.handle_status_change
        )

        self.control_panel.effectRunningChanged.connect(
            self.handle_effect_running
        )

        self.control_panel.lightStateRefreshRequested.connect(
            self.sync_light_state
        )

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setObjectName(
            "controlScrollArea"
        )
        self.scroll_area.setWidgetResizable(
            True
        )
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setFrameShape(
            QScrollArea.Shape.NoFrame
        )

        self.scroll_area.setWidget(
            self.control_panel
        )

        self.layout.addWidget(
            self.scroll_area
        )

        self.update_ui()

    def create_header(self) -> None:
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(
            4,
            0,
            4,
            2,
        )

        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)

        title_label = QLabel(
            "Yeelight Controller"
        )
        title_label.setObjectName(
            "windowTitle"
        )

        subtitle_label = QLabel(
            "Lightstrip Plus"
        )
        subtitle_label.setObjectName(
            "windowSubtitle"
        )

        title_layout.addWidget(
            title_label
        )
        title_layout.addWidget(
            subtitle_label
        )

        self.status_label = QLabel(
            "Connecting..."
        )
        self.status_label.setObjectName(
            "statusLabel"
        )

        self.power_button = QPushButton(
            "Turn On"
        )
        self.power_button.setObjectName(
            "powerButton"
        )
        self.power_button.clicked.connect(
            self.toggle_power
        )

        header_layout.addLayout(
            title_layout
        )
        header_layout.addStretch()
        header_layout.addWidget(
            self.status_label
        )
        header_layout.addSpacing(12)
        header_layout.addWidget(
            self.power_button
        )

        self.layout.addLayout(
            header_layout
        )

    def load_initial_state(self) -> None:
        try:
            state = self.controller.get_state()

            self.is_light_on = state.is_on

            self.control_panel.set_light_state(
                QColor(
                    state.red,
                    state.green,
                    state.blue,
                ),
                state.brightness,
            )

            self.effect_engine.sync_running_state(
                state.effect_running
            )

            self.update_ui()

        except YeelightControllerError as error:
            self.status_label.setText(
                f"● {error}"
            )

            self.control_panel.set_enabled(
                False
            )

    def update_ui(self) -> None:
        if self.is_light_on:
            self.status_label.setText(
                "● On"
            )
            self.power_button.setText(
                "Turn Off"
            )
        else:
            self.status_label.setText(
                "● Off"
            )
            self.power_button.setText(
                "Turn On"
            )

        self.control_panel.set_enabled(
            self.is_light_on
        )

    def toggle_power(self) -> None:
        try:
            if self.is_light_on:
                if self.effect_is_running:
                    self.control_panel.stop_effect()
                    self.effect_is_running = False

                self.controller.turn_off()
                self.is_light_on = False
            else:
                self.controller.turn_on()
                self.is_light_on = True

            self.update_ui()

        except YeelightControllerError as error:
            self.status_label.setText(
                f"● {error}"
            )

    def handle_effect_running(
        self,
        running: bool,
    ) -> None:
        self.effect_is_running = running

        if running:
            self.status_label.setText(
                "● Effect running"
            )
        else:
            self.sync_light_state()

        self.control_panel.set_enabled(
            self.is_light_on
        )

    def sync_light_state(self) -> None:
        try:
            state = self.controller.get_state()

            self.is_light_on = state.is_on

            self.control_panel.set_light_state(
                QColor(
                    state.red,
                    state.green,
                    state.blue,
                ),
                state.brightness,
            )

            self.update_ui()

        except YeelightControllerError as error:
            self.status_label.setText(
                f"● {error}"
            )

    def handle_status_change(
        self,
        status: str,
    ) -> None:
        if self.effect_is_running:
            return

        self.status_label.setText(
            status
        )