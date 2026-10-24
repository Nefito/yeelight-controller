from yeelight_controller.core.device_manager import DeviceConfig

DEFAULT_DEVICE_ID = "tv"

YEELIGHT_DEVICES = (
    DeviceConfig(
        id="tv",
        name="TV Lightstrip",
        ip_address="192.168.177.246",
        model="YLDD04YL",
    ),
    DeviceConfig(
        id="monitor",
        name="Monitor Lightstrip Pro",
        ip_address="192.168.177.107",
        model="YLDD005",
    ),
)
