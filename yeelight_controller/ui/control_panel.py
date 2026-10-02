from PySide6.QtCore import Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QGraphicsOpacityEffect,
    QVBoxLayout,
    QWidget,
)

from yeelight_controller.core.controller import YeelightController
from yeelight_controller.core.timers.timer_manager import TimerManager
from yeelight_controller.effects.engine import EffectEngine
from yeelight_controller.ui.brightness.brightness_control import (
    BrightnessControl,
)
from yeelight_controller.ui.color.color_control import ColorControl
from yeelight_controller.ui.color.color_presets import ColorPresets
from yeelight_controller.ui.effects.effects_control import EffectsControl
from yeelight_controller.ui.section_card import SectionCard
from yeelight_controller.ui.timers.timers_control import TimersControl


class ControlPanel(QWidget):
    statusChanged = Signal(str)
    effectRunningChanged = Signal(bool)
    lightStateRefreshRequested = Signal()

    def __init__(
        self,
        controller: YeelightController,
        effect_engine: EffectEngine,
        timer_manager: TimerManager,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)

        self.controller = controller
        self.effect_engine = effect_engine
        self.timer_manager = timer_manager

        self.setup_ui()
        self.create_opacity_effects()
        self.connect_signals()

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        self.create_color_section(layout)
        self.create_presets_section(layout)
        self.create_brightness_section(layout)
        self.create_effects_section(layout)
        self.create_timers_section(layout)

    def create_color_section(
        self,
        parent_layout: QVBoxLayout,
    ) -> None:
        section = SectionCard(
            "Color",
            self,
            collapsible=True,
            collapsed=True,
        )

        self.color_control = ColorControl(
            self.controller,
            QColor(255, 255, 255),
            self,
        )

        section.add_widget(
            self.color_control
        )

        parent_layout.addWidget(section)

    def create_presets_section(
        self,
        parent_layout: QVBoxLayout,
    ) -> None:
        section = SectionCard(
            "Presets",
            self,
        )

        self.color_presets = ColorPresets(
            self
        )

        section.add_widget(
            self.color_presets
        )

        parent_layout.addWidget(section)

    def create_brightness_section(
        self,
        parent_layout: QVBoxLayout,
    ) -> None:
        section = SectionCard(
            "Brightness",
            self,
        )

        self.brightness_control = BrightnessControl(
            self.controller,
            parent=self,
        )

        section.add_widget(
            self.brightness_control
        )

        parent_layout.addWidget(section)

    def create_effects_section(
        self,
        parent_layout: QVBoxLayout,
    ) -> None:
        section = SectionCard(
            "Effects",
            self,
        )

        self.effects_control = EffectsControl(
            self.effect_engine,
            self,
        )

        section.add_widget(
            self.effects_control
        )

        parent_layout.addWidget(section)

    def create_timers_section(
        self,
        parent_layout: QVBoxLayout,
    ) -> None:
        section = SectionCard(
            "Timers",
            self,
        )

        self.timers_control = TimersControl(
            self.timer_manager,
            self,
        )

        section.add_widget(
            self.timers_control
        )

        parent_layout.addWidget(section)

    def create_opacity_effects(self) -> None:
        self.color_control_effect = QGraphicsOpacityEffect(self)
        self.color_presets_effect = QGraphicsOpacityEffect(self)
        self.brightness_control_effect = QGraphicsOpacityEffect(self)
        self.effects_control_effect = QGraphicsOpacityEffect(self)
        self.timers_control_effect = QGraphicsOpacityEffect(self)

        self.color_control.setGraphicsEffect(
            self.color_control_effect
        )
        self.color_presets.setGraphicsEffect(
            self.color_presets_effect
        )
        self.brightness_control.setGraphicsEffect(
            self.brightness_control_effect
        )
        self.effects_control.setGraphicsEffect(
            self.effects_control_effect
        )
        self.timers_control.setGraphicsEffect(
            self.timers_control_effect
        )

    def connect_signals(self) -> None:
        self.color_control.statusChanged.connect(
            self.statusChanged
        )
        self.brightness_control.statusChanged.connect(
            self.statusChanged
        )
        self.timers_control.statusChanged.connect(
            self.statusChanged
        )
        self.timers_control.lightStateRefreshRequested.connect(
            self.lightStateRefreshRequested
        )
        self.color_presets.colorSelected.connect(
            self.color_control.request_color
        )
        self.effects_control.runningChanged.connect(
            self.handle_effect_running
        )

    def set_light_state(
        self,
        color: QColor,
        brightness: int,
    ) -> None:
        self.color_control.set_color(color)
        self.brightness_control.set_brightness(
            brightness
        )

    def set_enabled(
        self,
        enabled: bool,
    ) -> None:
        manual_controls_enabled = (
            enabled
            and not self.effect_engine.is_running()
        )

        self.color_control.setEnabled(
            manual_controls_enabled
        )
        self.color_presets.setEnabled(
            manual_controls_enabled
        )
        self.brightness_control.setEnabled(
            manual_controls_enabled
        )
        self.effects_control.setEnabled(
            enabled
        )
        self.timers_control.setEnabled(
            enabled
        )

        manual_opacity = (
            1.0
            if manual_controls_enabled
            else 0.45
        )
        enabled_opacity = (
            1.0
            if enabled
            else 0.45
        )

        self.color_control_effect.setOpacity(
            manual_opacity
        )
        self.color_presets_effect.setOpacity(
            manual_opacity
        )
        self.brightness_control_effect.setOpacity(
            manual_opacity
        )
        self.effects_control_effect.setOpacity(
            enabled_opacity
        )
        self.timers_control_effect.setOpacity(
            enabled_opacity
        )

    def stop_effect(self) -> None:
        self.effect_engine.stop()

    def handle_effect_running(
        self,
        running: bool,
    ) -> None:
        self.effectRunningChanged.emit(
            running
        )