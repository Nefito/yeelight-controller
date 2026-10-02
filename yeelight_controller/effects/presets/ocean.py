from yeelight import Flow, RGBTransition

from yeelight_controller.effects.base import Effect


class OceanEffect(Effect):
    name = "Ocean"
    default_speed = 0.45

    def create_flow(self, speed: float) -> Flow:
        duration = int(1800 / speed)

        transitions = [
            RGBTransition(
                0,
                80,
                180,
                duration=duration,
                brightness=65,
            ),
            RGBTransition(
                0,
                180,
                255,
                duration=duration,
                brightness=75,
            ),
            RGBTransition(
                20,
                80,
                200,
                duration=duration,
                brightness=60,
            ),
            RGBTransition(
                0,
                150,
                220,
                duration=duration,
                brightness=70,
            ),
        ]

        return Flow(
            count=0,
            action=Flow.actions.stay,
            transitions=transitions,
        )