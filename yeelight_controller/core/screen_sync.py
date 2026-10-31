"""Four-region monitor backlight streaming for the YLDD005 Lightstrip Pro."""

import json
import math
import socket
import threading
import time

import mss
from PIL import Image
from PySide6.QtCore import QThread, Signal


class ScreenSyncWorker(QThread):
    statusChanged = Signal(str)
    syncStopped = Signal(str)

    FPS = 20
    EDGE_DEPTH = 0.12
    CORNER_EXCLUSION = 0.15
    SMALL_TIME_CONSTANT = 0.30
    LARGE_TIME_CONSTANT = 0.09
    CHANGE_THRESHOLD = 65
    MIN_BRIGHTNESS = 8
    MUSIC_PORT = 54322

    def __init__(self, strip_ip: str, monitor_index: int = 1, parent=None):
        super().__init__(parent)
        self.strip_ip = strip_ip
        self.monitor_index = monitor_index
        self._stop_event = threading.Event()

    def request_stop(self):
        self._stop_event.set()

    @staticmethod
    def _send(sock, command_id, method, params):
        message = json.dumps(
            {"id": command_id, "method": method, "params": params},
            separators=(",", ":"),
        )
        sock.sendall((message + "\r\n").encode("utf-8"))

    @staticmethod
    def _read_response(sock, command_id):
        data = b""
        while b"\n" not in data:
            chunk = sock.recv(4096)
            if not chunk:
                raise ConnectionError("Strip closed the control connection.")
            data += chunk
        for line in data.splitlines():
            if line.strip():
                response = json.loads(line)
                if response.get("id") == command_id:
                    return response
        raise ConnectionError("Missing Music Mode response.")

    def _stop_music_mode(self):
        try:
            with socket.create_connection((self.strip_ip, 55443), timeout=2) as sock:
                sock.settimeout(2)
                self._send(sock, 9999, "set_music", [0])
        except OSError:
            pass

    @staticmethod
    def _average(image, bounds):
        return (
            image.crop(bounds)
            .resize((24, 24), Image.Resampling.BOX)
            .resize((1, 1), Image.Resampling.BOX)
            .getpixel((0, 0))
        )

    def _sample(self, image):
        width, height = image.size
        edge_x = max(1, int(width * self.EDGE_DEPTH))
        edge_y = max(1, int(height * self.EDGE_DEPTH))
        corner_x = int(width * self.CORNER_EXCLUSION)
        corner_y = int(height * self.CORNER_EXCLUSION)

        top = self._average(image, (corner_x, 0, width - corner_x, edge_y))
        right = self._average(
            image, (width - edge_x, corner_y, width, height - corner_y)
        )
        bottom = self._average(
            image, (corner_x, height - edge_y, width - corner_x, height)
        )
        left = self._average(image, (0, corner_y, edge_x, height - corner_y))
        # Confirmed physical mapping: bottom, right, top, left.
        return [bottom, right, top, left]

    def _smooth(self, previous, current, dt):
        if previous is None:
            return [tuple(map(float, color)) for color in current]

        output = []
        for old, new in zip(previous, current):
            distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(old, new)))
            tau = (
                self.LARGE_TIME_CONSTANT
                if distance >= self.CHANGE_THRESHOLD
                else self.SMALL_TIME_CONSTANT
            )
            alpha = 1 - math.exp(-max(0, dt) / tau)
            output.append(
                tuple(a + (b - a) * alpha for a, b in zip(old, new))
            )
        return output

    def _effect_params(self, colors):
        packed = []
        for color in colors:
            channels = [max(0, min(255, round(value))) for value in color]
            maximum = max(channels)
            if 0 < maximum < self.MIN_BRIGHTNESS:
                channels = [
                    min(255, round(value * self.MIN_BRIGHTNESS / maximum))
                    for value in channels
                ]
            red, green, blue = channels
            packed.append(str((red << 16) | (green << 8) | blue))

        # Keep the exact known-working four-color firmware payload.
        effect = "0,100,255,100,254,4," + ",".join(packed) + ","
        return [1, 0, effect]

    def run(self):
        reason = ""
        music_started = False
        try:
            with mss.mss() as capture:
                if not 0 <= self.monitor_index < len(capture.monitors):
                    raise ValueError("Selected monitor is unavailable.")
                monitor = capture.monitors[self.monitor_index]

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
                    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    server.bind(("0.0.0.0", self.MUSIC_PORT))
                    server.listen(1)
                    server.settimeout(0.5)

                    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as probe:
                        probe.connect((self.strip_ip, 55443))
                        local_ip = probe.getsockname()[0]

                    with socket.create_connection(
                        (self.strip_ip, 55443), timeout=3
                    ) as control:
                        control.settimeout(3)
                        self._send(
                            control, 1, "set_music",
                            [1, local_ip, self.MUSIC_PORT],
                        )
                        response = self._read_response(control, 1)
                        if response.get("result") != ["ok"]:
                            raise ConnectionError(
                                f"Music Mode rejected: {response}"
                            )
                        music_started = True

                    self.statusChanged.emit("Waiting for strip...")
                    connection = None
                    while not self._stop_event.is_set() and connection is None:
                        try:
                            connection, _ = server.accept()
                        except socket.timeout:
                            continue

                    if connection is not None:
                        with connection:
                            self.statusChanged.emit("Screen sync running")
                            previous = None
                            last_frame = time.monotonic()
                            next_frame = last_frame
                            frame_id = 2
                            while not self._stop_event.is_set():
                                now = time.monotonic()
                                dt = now - last_frame
                                last_frame = now

                                shot = capture.grab(monitor)
                                image = Image.frombytes(
                                    "RGB", shot.size, shot.rgb
                                )
                                previous = self._smooth(
                                    previous, self._sample(image), dt
                                )
                                self._send(
                                    connection, frame_id, "set_fx",
                                    self._effect_params(previous),
                                )
                                frame_id += 1

                                next_frame += 1 / self.FPS
                                delay = next_frame - time.monotonic()
                                if delay > 0:
                                    self._stop_event.wait(delay)
                                else:
                                    next_frame = time.monotonic()
        except (OSError, ValueError, ConnectionError, json.JSONDecodeError) as exc:
            reason = str(exc)
        finally:
            if music_started:
                self._stop_music_mode()
            self.syncStopped.emit(reason)
