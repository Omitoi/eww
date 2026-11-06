#!/usr/bin/env python3
import glob
import json
import os
import subprocess
import time

def get_device_info(mac):
    """Return paired/trusted/connected flags for a given MAC via bluetoothctl info."""
    paired = False
    trusted = False
    connected = False
    try:
        info = subprocess.check_output(["bluetoothctl", "info", mac], text=True, timeout=2)
        for line in info.splitlines():
            line = line.strip()
            if line.startswith("Paired:"):
                paired = "yes" in line
            elif line.startswith("Trusted:"):
                trusted = "yes" in line
            elif line.startswith("Connected:"):
                connected = "yes" in line
    except Exception:
        pass
    return paired, trusted, connected

def get_bt_list():
    if not os.path.exists("/sys/class/bluetooth") or not glob.glob("/sys/class/bluetooth/hci*"):
        return json.dumps({
            "empty": True,
            "devices": [],
            "message": "No Bluetooth adapter"
        })

    try:
        out = subprocess.check_output(["bluetoothctl", "devices"], text=True, timeout=2)

        raw = [
            line.strip().split(" ", 2)
            for line in out.splitlines()
            if len(line.strip().split(" ", 2)) >= 3
        ]

        devs = []
        for parts in raw:
            mac = parts[1]
            name = parts[2]
            paired, trusted, connected = get_device_info(mac)
            devs.append({
                "mac": mac,
                "name": name,
                "connected": connected,
                "paired": paired,
                "trusted": trusted,
            })

        if not devs:
            # Trigger active scan in background if no devices found
            subprocess.Popen(["bluetoothctl", "--timeout", "5", "scan", "on"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return json.dumps({
                "empty": True,
                "devices": [],
                "message": "No devices found\nscanning..."
            })

        return json.dumps({
            "empty": False,
            "devices": devs,
            "message": ""
        })
    except Exception:
        return json.dumps({
            "empty": True,
            "devices": [],
            "message": "No devices found\nscanning..."
        })

if __name__ == "__main__":
    print(get_bt_list())
