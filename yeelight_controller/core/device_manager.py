from dataclasses import dataclass

from yeelight_controller.core.controller import YeelightController


@dataclass(frozen=True)
class DeviceConfig:
    id: str
    name: str
    ip_address: str
    model: str


class DeviceManager:
    """Maintain one controller per configured Yeelight device."""

    def __init__(self, devices: tuple[DeviceConfig, ...]):
        if not devices:
            raise ValueError("At least one device must be configured.")

        ids = [device.id for device in devices]
        if len(ids) != len(set(ids)):
            raise ValueError("Device IDs must be unique.")

        self._devices = {device.id: device for device in devices}
        self._controllers = {
            device.id: YeelightController(device.ip_address)
            for device in devices
        }

    def list_devices(self) -> tuple[DeviceConfig, ...]:
        return tuple(self._devices.values())

    def get_device(self, device_id: str) -> DeviceConfig:
        return self._devices[device_id]

    def get_controller(self, device_id: str) -> YeelightController:
        return self._controllers[device_id]
