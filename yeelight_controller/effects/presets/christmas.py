from yeelight import Flow
from yeelight.flows import christmas

from yeelight_controller.effects.base import Effect


class ChristmasEffect(Effect):
    name = "Christmas"
    default_speed = 0.75

    def create_flow(self, speed: float) -> Flow:
        duration = max(
            50,
            int(250 / speed),
        )

        sleep = max(
            250,
            int(3000 / speed),
        )

        return christmas(
            duration=duration,
            brightness=100,
            sleep=sleep,
        )