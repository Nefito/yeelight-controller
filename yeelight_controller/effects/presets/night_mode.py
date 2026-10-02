from yeelight import Flow
from yeelight.flows import night_mode

from yeelight_controller.effects.base import Effect


class NightModeEffect(Effect):
    name = "Night Mode"
    supports_speed = False
    default_speed = 1.0

    def create_flow(self, speed: float) -> Flow:
        del speed

        return night_mode()