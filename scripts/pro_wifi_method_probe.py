"""Conservative Yeelight Pro TCP method-recognition probe.

Run from the repository root:
    python -m scripts.pro_wifi_method_probe

Only probes named candidate methods with empty parameter arrays.
This is experimental: undocumented methods may behave unexpectedly.
Do not run while another lighting controller or synchronization mode is active.
"""

import json
import socket
import time

from config import YEELIGHT_DEVICES

# Names are hypotheses, not verified YLDD005 TCP capabilities.
METHODS = (
    "__chatgpt_probe_nonexistent_method__",
    "set_pc_linkage",
    "set_rgb_pc",
    "set_pc_available",
    "udp_sess_new",
    "udp_chroma_sess_new",
)


def send_probe(ip: str, command_id: int, method: str) -> dict:
    request = json.dumps(
        {"id": command_id, "method": method, "params": []}
    ).encode("utf-8") + b"\r\n"

    with socket.create_connection((ip, 55443), timeout=5) as sock:
        sock.settimeout(5)
        sock.sendall(request)
        data = b""
        while b"\r\n" not in data:
            chunk = sock.recv(4096)
            if not chunk:
                raise ConnectionError("Connection closed before response")
            data += chunk
            if len(data) > 65536:
                raise ValueError("Response too large")

    for line in data.split(b"\r\n"):
        if not line.strip():
            continue
        message = json.loads(line)
        if message.get("id") == command_id:
            return message
    raise ValueError("No response with matching command ID")


def main() -> None:
    device = next(
        (entry for entry in YEELIGHT_DEVICES if entry.id == "monitor"),
        None,
    )
    if device is None:
        raise SystemExit("Monitor device is not configured.")

    print(f"Probing TCP method recognition at {device.ip_address}:55443")
    print("WARNING: Experimental undocumented commands; ensure no sync is running.")
    confirmation = input("Proceed with empty-parameter probes? [y/N]: ").strip().lower()
    if confirmation != "y":
        print("Cancelled.")
        return

    for index, method in enumerate(METHODS, start=1):
        print(f"\n{method}:")
        try:
            response = send_probe(device.ip_address, index, method)
            print(json.dumps(response, indent=2))
        except (OSError, ValueError) as error:
            print(f"Error: {error}")
        time.sleep(1)


if __name__ == "__main__":
    main()
