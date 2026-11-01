#!/usr/bin/env python3
"""Join dongle 7 to a Tello. No takeoff.

    .venv\\Scripts\\python.exe connect.py 10
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "core"))

from tello_dongle_setup import (  # noqa: E402
    REGISTRY_PATH,
    load_registry,
    windows_ipv4,
    windows_join,
)

DONGLE_NUMBER = 7


def main():
    drone_number = sys.argv[1] if len(sys.argv) > 1 else "10"
    ssid = drone_number if drone_number.upper().startswith("TELLO-") else f"TELLO-{drone_number}"
    registry = load_registry(REGISTRY_PATH)
    entry = next((item for item in registry["dongles"] if item.get("number") == DONGLE_NUMBER), None)
    if entry is None:
        raise SystemExit(f"dongle {DONGLE_NUMBER} is not in {REGISTRY_PATH}")
    iface = entry["iface"]
    print(f"dongle {DONGLE_NUMBER} on {iface} joining {ssid}", flush=True)
    deadline = time.time() + 45
    while time.time() < deadline:
        if windows_join(iface, ssid):
            print(f"connected {ssid} on {iface} at {windows_ipv4(iface)}", flush=True)
            return
        time.sleep(2)
    raise SystemExit(f"{ssid} did not come up on dongle {DONGLE_NUMBER}")


if __name__ == "__main__":
    main()
