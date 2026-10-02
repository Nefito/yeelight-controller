from yeelight import Flow
from yeelight.flows import sunrise

from yeelight_controller.effects.base import Effect


class SunriseEffect(Effect):
    name = "Sunrise"
    supports_speed = False
    default_speed = 1.0

    def create_flow(self, speed: float) -> Flow:
        del speed

        return sunrise()