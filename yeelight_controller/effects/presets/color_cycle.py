from yeelight import Flow, RGBTransition

from yeelight_controller.effects.base import Effect


class ColorCycleEffect(Effect):
    name = "Color Cycle"
    default_speed = 0.85

    def create_flow(self, speed: float) -> Flow:
        duration = int(1200 / speed)

        transitions = [
            RGBTransition(
                255,
                0,
                0,
                duration=duration,
            ),
            RGBTransition(
                255,
                128,
                0,
                duration=duration,
            ),
            RGBTransition(
                255,
                255,
                0,
                duration=duration,
            ),
            RGBTransition(
                0,
                255,
                0,
                duration=duration,
            ),
            RGBTransition(
                0,
                255,
                255,
                duration=duration,
            ),
            RGBTransition(
                0,
                0,
                255,
                duration=duration,
            ),
            RGBTransition(
                128,
                0,
                255,
                duration=duration,
            ),
            RGBTransition(
                255,
                0,
                255,
                duration=duration,
            ),
        ]

        return Flow(
            count=0,
            action=Flow.actions.stay,
            transitions=transitions,
        )