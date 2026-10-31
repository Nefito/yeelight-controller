"""Read-only Yeelight SSDP capability discovery for the configured monitor strip.

Run from the project root:
    python -m scripts.pro_discover_capabilities

Sends only a standard multicast discovery request; never changes lighting.
Discovery may fail across Wi-Fi mesh segments even when TCP LAN control works.
"""

import socket
from config import YEELIGHT_DEVICES

DISCOVERY_ADDRESS = ("239.255.255.250", 1982)
DISCOVERY_REQUEST = (
    "M-SEARCH * HTTP/1.1\r\n"
    "HOST: 239.255.255.250:1982\r\n"
    'MAN: "ssdp:discover"\r\n'
    "ST: wifi_bulb\r\n"
    "\r\n"
).encode("ascii")


def main() -> None:
    monitor = next(
        (device for device in YEELIGHT_DEVICES if device.id == "monitor"),
        None,
    )
    if monitor is None:
        raise SystemExit("No monitor device configured.")

    print(f"Looking for {monitor.name} at {monitor.ip_address}")
    print("Sending read-only Yeelight discovery request...")

    matches = []
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(3)
            sock.sendto(DISCOVERY_REQUEST, DISCOVERY_ADDRESS)

            while True:
                try:
                    data, address = sock.recvfrom(8192)
                except socket.timeout:
                    break

                if address[0] != monitor.ip_address:
                    continue

                headers = {}
                for line in data.decode("utf-8", errors="replace").splitlines():
                    if ":" in line:
                        key, value = line.split(":", 1)
                        headers[key.strip().lower()] = value.strip()
                matches.append(headers)

    except OSError as error:
        print(f"Discovery failed: {error}")
        return

    if not matches:
        print("No discovery response from the monitor strip.")
        print("This does not mean the strip lacks LAN capabilities.")
        print("Multicast discovery can be blocked by routers or mesh Wi-Fi.")
        return

    for index, headers in enumerate(matches, start=1):
        print(f"\nResponse {index}:")
        for key in ("location", "id", "model", "fw_ver", "support"):
            print(f"  {key}: {headers.get(key, '(not reported)')}")


if __name__ == "__main__":
    main()
