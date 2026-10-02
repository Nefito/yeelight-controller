from typing import ClassVar

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from yeelight_controller.core.debouncer import DebouncedAction
from yeelight_controller.effects.base import Effect
from yeelight_controller.effects.engine import EffectEngine
from yeelight_controller.effects.presets.christmas import (
    ChristmasEffect,
)
from yeelight_controller.effects.presets.color_cycle import (
    ColorCycleEffect,
)
from yeelight_controller.effects.presets.disco import DiscoEffect
from yeelight_controller.effects.presets.lsd import LSDEffect
from yeelight_controller.effects.presets.night_mode import (
    NightModeEffect,
)
from yeelight_controller.effects.presets.ocean import OceanEffect
from yeelight_controller.effects.presets.purple_dream import (
    PurpleDreamEffect,
)
from yeelight_controller.effects.presets.sunrise import (
    SunriseEffect,
)
from yeelight_controller.effects.presets.sunset import (
    SunsetEffect,
)
from yeelight_controller.effects.presets.warm_flicker import (
    WarmFlickerEffect,
)


class EffectsControl(QWidget):
    statusChanged = Signal(str)
    runningChanged = Signal(bool)

    EFFECTS: ClassVar[list[type[Effect]]] = [
        ColorCycleEffect,
        WarmFlickerEffect,
        OceanEffect,
        PurpleDreamEffect,
        LSDEffect,
        DiscoEffect,
        ChristmasEffect,
        NightModeEffect,
        SunriseEffect,
        SunsetEffect,
    ]

    def __init__(
        self,
        engine: EffectEngine,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)

        self.engine = engine

        self.speed_update_action = DebouncedAction(
            self.apply_pending_speed,
            interval=200,
            parent=self,
        )

        self.setup_ui()
        self.connect_signals()

        self.sync_speed_to_selected_effect()

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        layout.setSpacing(10)

        effect_layout = QHBoxLayout()
        effect_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        effect_layout.setSpacing(8)

        effect_label = QLabel("Effect")
        effect_label.setObjectName(
            "effectLabel"
        )

        self.effect_selector = QComboBox()
        self.effect_selector.setObjectName(
            "effectSelector"
        )

        for effect_class in self.EFFECTS:
            self.effect_selector.addItem(
                effect_class.name,
                effect_class,
            )

        self.toggle_button = QPushButton(
            "Start"
        )
        self.toggle_button.setObjectName(
            "effectButton"
        )

        effect_layout.addWidget(
            effect_label
        )
        effect_layout.addWidget(
            self.effect_selector,
            1,
        )
        effect_layout.addWidget(
            self.toggle_button
        )

        self.speed_section = QWidget()

        speed_layout = QVBoxLayout(
            self.speed_section
        )
        speed_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        speed_layout.setSpacing(6)

        speed_title_layout = QHBoxLayout()
        speed_title_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        speed_label = QLabel("Speed")
        speed_label.setObjectName(
            "effectLabel"
        )

        self.speed_value = QLabel()
        self.speed_value.setObjectName(
            "effectSpeedValue"
        )

        speed_title_layout.addWidget(
            speed_label
        )
        speed_title_layout.addStretch()
        speed_title_layout.addWidget(
            self.speed_value
        )

        self.speed_slider = QSlider(
            Qt.Orientation.Horizontal
        )
        self.speed_slider.setRange(
            25,
            200,
        )
        self.speed_slider.setMinimumHeight(
            24
        )

        speed_layout.addLayout(
            speed_title_layout
        )
        speed_layout.addWidget(
            self.speed_slider
        )

        self.status_label = QLabel(
            "● Stopped"
        )
        self.status_label.setObjectName(
            "effectStatus"
        )

        layout.addLayout(
            effect_layout
        )
        layout.addWidget(
            self.speed_section
        )
        layout.addWidget(
            self.status_label
        )

    def connect_signals(self) -> None:
        self.toggle_button.clicked.connect(
            self.toggle_effect
        )

        self.effect_selector.currentIndexChanged.connect(
            self.handle_effect_selection_changed
        )

        self.speed_slider.valueChanged.connect(
            self.handle_speed_changed
        )

        self.engine.runningChanged.connect(
            self.handle_running_changed
        )

        self.engine.errorOccurred.connect(
            self.handle_error
        )

    def toggle_effect(self) -> None:
        if self.engine.is_running():
            self.engine.stop()
            return

        effect = self.create_selected_effect()

        if effect.supports_speed:
            self.apply_pending_speed()

        self.engine.start(effect)

    def create_selected_effect(self) -> Effect:
        effect_class = (
            self.effect_selector.currentData()
        )

        return effect_class()

    def handle_effect_selection_changed(
        self,
        index: int,
    ) -> None:
        del index

        if self.engine.is_running():
            return

        self.sync_speed_to_selected_effect()

    def sync_speed_to_selected_effect(self) -> None:
        effect_class = (
            self.effect_selector.currentData()
        )

        supports_speed = effect_class.supports_speed

        self.speed_section.setVisible(
            supports_speed
        )

        if not supports_speed:
            return

        default_speed = effect_class.default_speed
        slider_value = round(
            default_speed * 100
        )

        self.speed_slider.blockSignals(True)
        self.speed_slider.setValue(
            slider_value
        )
        self.speed_slider.blockSignals(False)

        self.speed_value.setText(
            self.get_speed_label(
                default_speed
            )
        )

    def handle_speed_changed(
        self,
        value: int,
    ) -> None:
        if not self.can_change_speed():
            return

        speed = value / 100

        self.speed_value.setText(
            self.get_speed_label(speed)
        )

        self.speed_update_action.start()

    def apply_pending_speed(self) -> None:
        if not self.can_change_speed():
            return

        speed = (
            self.speed_slider.value()
            / 100
        )

        self.engine.set_speed(speed)

    def can_change_speed(self) -> bool:
        if self.engine.is_running():
            if self.engine.effect is None:
                return False

            return self.engine.effect.supports_speed

        effect_class = (
            self.effect_selector.currentData()
        )

        return effect_class.supports_speed

    def get_speed_label(
        self,
        speed: float,
    ) -> str:
        if speed < 0.5:
            return "Very Slow"

        if speed < 0.85:
            return "Slow"

        if speed < 1.25:
            return "Normal"

        if speed < 1.7:
            return "Fast"

        return "Very Fast"

    def handle_running_changed(
        self,
        running: bool,
    ) -> None:
        if running:
            self.toggle_button.setText(
                "Stop"
            )
            self.effect_selector.setEnabled(
                False
            )

            if self.engine.effect is None:
                self.handle_unknown_effect_running()
            else:
                self.handle_known_effect_running()

        else:
            self.toggle_button.setText(
                "Start"
            )
            self.effect_selector.setEnabled(
                True
            )

            self.speed_slider.setEnabled(
                True
            )

            self.speed_section.setEnabled(
                True
            )

            self.status_label.setText(
                "● Stopped"
            )

            self.sync_speed_to_selected_effect()

        self.runningChanged.emit(running)

    def handle_known_effect_running(self) -> None:
        effect = self.engine.effect

        if effect is None:
            return

        self.speed_slider.setEnabled(
            effect.supports_speed
        )

        self.speed_section.setEnabled(
            effect.supports_speed
        )

        self.status_label.setText(
            f"● {effect.name}"
        )

    def handle_unknown_effect_running(self) -> None:
        self.speed_slider.setEnabled(
            False
        )

        self.speed_section.setEnabled(
            False
        )

        self.status_label.setText(
            "● Unknown effect running"
        )

    def handle_error(
        self,
        message: str,
    ) -> None:
        self.status_label.setText(
            f"● {message}"
        )