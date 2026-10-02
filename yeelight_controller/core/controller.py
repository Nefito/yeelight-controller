from dataclasses import dataclass
from typing import Any

from yeelight import Bulb, CronType
from yeelight.main import BulbException


class YeelightControllerError(Exception):
    """Raised when communication with the Yeelight fails."""


@dataclass
class LightState:
    is_on: bool
    red: int
    green: int
    blue: int
    brightness: int
    effect_running: bool


class YeelightController:
    def __init__(self, ip_address: str):
        self.bulb = Bulb(ip_address)

    def turn_on(self) -> None:
        try:
            self.bulb.turn_on()
        except BulbException as error:
            raise YeelightControllerError(
                "Failed to turn the light on."
            ) from error

    def turn_off(self) -> None:
        try:
            self.bulb.turn_off()
        except BulbException as error:
            raise YeelightControllerError(
                "Failed to turn the light off."
            ) from error

    def set_color(
        self,
        red: int,
        green: int,
        blue: int,
        effect: str = "smooth",
        duration: int = 300,
    ) -> None:
        if red == 0 and green == 0 and blue == 0:
            raise YeelightControllerError(
                "Black is not supported by the lightstrip."
            )

        try:
            self.bulb.set_rgb(
                red,
                green,
                blue,
                effect=effect,
                duration=duration,
            )
        except BulbException as error:
            raise YeelightControllerError(
                "Failed to change the light color."
            ) from error

    def set_brightness(
        self,
        brightness: int,
    ) -> None:
        try:
            self.bulb.set_brightness(
                brightness
            )
        except BulbException as error:
            raise YeelightControllerError(
                "Failed to change the brightness."
            ) from error

    def start_flow(
        self,
        flow,
    ) -> None:
        try:
            self.bulb.start_flow(flow)
        except BulbException as error:
            raise YeelightControllerError(
                "Failed to start the light effect."
            ) from error

    def stop_flow(self) -> None:
        try:
            self.bulb.stop_flow()
        except BulbException as error:
            raise YeelightControllerError(
                "Failed to stop the light effect."
            ) from error

    def set_off_timer(
        self,
        minutes: int,
    ) -> None:
        if minutes <= 0:
            raise ValueError(
                "Timer duration must be greater than zero."
            )

        try:
            self.bulb.cron_add(
                CronType.off,
                minutes,
            )
        except BulbException as error:
            raise YeelightControllerError(
                "Failed to set the turn-off timer."
            ) from error

    def get_off_timer(
        self,
    ) -> dict[str, Any] | None:
        try:
            return self.bulb.cron_get(
                CronType.off
            )
        except BulbException as error:
            raise YeelightControllerError(
                "Failed to get the turn-off timer."
            ) from error

    def cancel_off_timer(self) -> None:
        try:
            self.bulb.cron_del(
                CronType.off
            )
        except BulbException as error:
            raise YeelightControllerError(
                "Failed to cancel the turn-off timer."
            ) from error

    def get_state(self) -> LightState:
        try:
            properties = self.bulb.get_properties(
                [
                    "power",
                    "rgb",
                    "bright",
                    "flowing",
                ]
            )
        except BulbException as error:
            raise YeelightControllerError(
                "Failed to get the light state."
            ) from error

        rgb = int(
            properties.get("rgb", 0)
        )

        red = (rgb >> 16) & 0xFF
        green = (rgb >> 8) & 0xFF
        blue = rgb & 0xFF

        return LightState(
            is_on=(
                properties.get("power")
                == "on"
            ),
            red=red,
            green=green,
            blue=blue,
            brightness=int(
                properties.get(
                    "bright",
                    100,
                )
            ),
            effect_running=(
                int(
                    properties.get(
                        "flowing",
                        0,
                    )
                )
                == 1
            ),
        )