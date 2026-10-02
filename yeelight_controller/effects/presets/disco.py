from yeelight import Flow
from yeelight.flows import disco

from yeelight_controller.effects.base import Effect


class DiscoEffect(Effect):
    name = "Disco"
    default_speed = 1.0

    def create_flow(self, speed: float) -> Flow:
        bpm = max(
            30,
            min(
                240,
                round(120 * speed),
            ),
        )

        return disco(bpm=bpm)