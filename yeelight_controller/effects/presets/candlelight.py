from yeelight import Flow
from yeelight.flows import candle_flicker

from yeelight_controller.effects.base import Effect


class CandlelightEffect(Effect):
    name = "Candlelight"
    default_speed = 0.5

    def create_flow(self, speed: float) -> Flow:
        del speed

        return candle_flicker()