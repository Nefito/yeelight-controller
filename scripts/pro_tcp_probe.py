"""Read-only TCP protocol probe for Yeelight Lightstrip Pro.

Run from project root:
    python -m scripts.pro_tcp_probe

Sends standard get_prop and an intentionally nonexistent method.
No lighting settings are modified.
"""

import json
import socket

from config import YEELIGHT_DEVICES


def request(ip: str, command_id: int, method: str, params: list) -> dict:
    payload = json.dumps({
        "id": command_id,
        "method": method,
        "params": params,
    }).encode("utf-8") + b"\r\n"

    with socket.create_connection((ip, 55443), timeout=5) as connection:
        connection.settimeout(5)
        connection.sendall(payload)
        buffer = b""
        while b"\r\n" not in buffer:
            chunk = connection.recv(4096)
            if not chunk:
                raise ConnectionError("Device closed the connection.")
            buffer += chunk
            if len(buffer) > 65536:
                raise ValueError("Response too large.")

    for line in buffer.split(b"\r\n"):
        if not line.strip():
            continue
        response = json.loads(line)
        if response.get("id") == command_id:
            return response

    raise ValueError("No response with matching command ID.")


def main() -> None:
    device = next(
        (item for item in YEELIGHT_DEVICES if item.id == "monitor"),
        None,
    )
    if device is None:
        raise SystemExit("Monitor lightstrip is not configured.")

    tests = (
        (1, "get_prop", ["power", "color_mode"]),
        (2, "__chatgpt_probe_nonexistent_method__", []),
    )
    for command_id, method, params in tests:
        print(f"\nMethod: {method}")
        try:
            response = request(device.ip_address, command_id, method, params)
            print(json.dumps(response, indent=2))
        except (OSError, ValueError) as error:
            print(f"Probe failed: {error}")


if __name__ == "__main__":
    main()
