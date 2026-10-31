"""Read-only Yeelight Lightstrip Pro LAN diagnostics.

Run from the project root:
    python scripts/pro_lan_diagnostics.py

This script sends only the standard Yeelight get_prop request.
It does not change power, color, brightness, effects, or timers.
"""

import json
import socket

from config import YEELIGHT_DEVICES

PROPERTY_NAMES = [
    "power", "bright", "ct", "rgb", "hue", "sat",
    "color_mode", "flowing", "flow_params", "music_on",
    "name", "bg_power", "bg_bright", "bg_rgb",
    "active_mode", "nl_br",
]


def main() -> None:
    device = next(
        (item for item in YEELIGHT_DEVICES if item.id == "monitor"),
        None,
    )
    if device is None:
        raise SystemExit("Monitor lightstrip not configured.")

    request = {
        "id": 1,
        "method": "get_prop",
        "params": PROPERTY_NAMES,
    }

    print(f"Device: {device.name} ({device.model})")
    print(f"Address: {device.ip_address}:55443")
    print("Command: get_prop (read-only)")
    print()

    try:
        with socket.create_connection(
            (device.ip_address, 55443), timeout=5
        ) as connection:
            connection.settimeout(5)
            payload = json.dumps(request) + "\r\n"
            connection.sendall(payload.encode("utf-8"))

            buffer = b""
            while b"\r\n" not in buffer:
                chunk = connection.recv(4096)
                if not chunk:
                    raise ConnectionError(
                        "Connection closed before a complete response."
                    )
                buffer += chunk
                if len(buffer) > 65536:
                    raise ValueError("Response exceeds safety limit.")

        for line in buffer.split(b"\r\n"):
            if not line.strip():
                continue
            response = json.loads(line)
            if response.get("id") != request["id"]:
                print("Notification:", json.dumps(response, indent=2))
                continue
            if "error" in response:
                print("Device returned an error:")
                print(json.dumps(response["error"], indent=2))
                return

            values = response.get("result", [])
            print("Properties:")
            for name, value in zip(PROPERTY_NAMES, values):
                print(f"  {name}: {value!r}")
            if len(values) != len(PROPERTY_NAMES):
                print(
                    f"Warning: expected {len(PROPERTY_NAMES)} values, "
                    f"received {len(values)}."
                )
            return

        print("No matching response received.")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Diagnostic failed: {error}")


if __name__ == "__main__":
    main()
