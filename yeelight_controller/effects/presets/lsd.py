from yeelight import Flow
from yeelight.flows import lsd

from yeelight_controller.effects.base import Effect


class LSDEffect(Effect):
    name = "LSD"
    default_speed = 0.65

    def create_flow(self, speed: float) -> Flow:
        duration = int(3000 / speed)

        return lsd(
            duration=duration,
            brightness=100,
        )