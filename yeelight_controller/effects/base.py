from abc import ABC, abstractmethod

from yeelight import Flow


class Effect(ABC):
    name: str
    supports_speed: bool = True
    default_speed: float = 1.0

    @abstractmethod
    def create_flow(self, speed: float) -> Flow:
        """Create a Yeelight flow for this effect."""
        raise NotImplementedError