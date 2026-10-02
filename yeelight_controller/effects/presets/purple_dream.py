from yeelight import Flow, RGBTransition

from yeelight_controller.effects.base import Effect


class PurpleDreamEffect(Effect):
    name = "Purple Dream"
    default_speed = 0.65

    def create_flow(self, speed: float) -> Flow:
        duration = int(2000 / speed)

        transitions = [
            RGBTransition(
                90,
                20,
                160,
                duration=duration,
                brightness=60,
            ),
            RGBTransition(
                180,
                30,
                200,
                duration=duration,
                brightness=70,
            ),
            RGBTransition(
                90,
                20,
                180,
                duration=duration,
                brightness=55,
            ),
            RGBTransition(
                220,
                50,
                180,
                duration=duration,
                brightness=65,
            ),
        ]

        return Flow(
            count=0,
            action=Flow.actions.stay,
            transitions=transitions,
        )