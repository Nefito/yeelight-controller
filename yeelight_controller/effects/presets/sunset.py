from yeelight import Flow
from yeelight.flows import sunset

from yeelight_controller.effects.base import Effect


class SunsetEffect(Effect):
    name = "Sunset"
    supports_speed = False
    default_speed = 1.0

    def create_flow(self, speed: float) -> Flow:
        del speed

        return sunset()