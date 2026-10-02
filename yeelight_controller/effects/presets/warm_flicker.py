from yeelight import Flow, RGBTransition

from yeelight_controller.effects.base import Effect


class WarmFlickerEffect(Effect):
    name = "Warm Flicker"
    default_speed = 0.35

    def create_flow(self, speed: float) -> Flow:
        base_duration = int(900 / speed)

        transitions = [
            RGBTransition(
                255,
                90,
                20,
                duration=base_duration,
                brightness=65,
            ),
            RGBTransition(
                255,
                140,
                35,
                duration=int(base_duration * 0.7),
                brightness=80,
            ),
            RGBTransition(
                255,
                70,
                10,
                duration=int(base_duration * 0.5),
                brightness=55,
            ),
            RGBTransition(
                255,
                160,
                45,
                duration=int(base_duration * 0.8),
                brightness=75,
            ),
            RGBTransition(
                255,
                95,
                15,
                duration=int(base_duration * 0.6),
                brightness=60,
            ),
            RGBTransition(
                255,
                130,
                25,
                duration=base_duration,
                brightness=70,
            ),
        ]

        return Flow(
            count=0,
            action=Flow.actions.stay,
            transitions=transitions,
        )