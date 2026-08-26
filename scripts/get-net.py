#!/usr/bin/env python3
import json, subprocess

try:
    res = subprocess.check_output(["iwctl", "station", "wlan0", "show"], text=True)
    ssid = next((line.split("Connected network", 1)[1].strip() for line in res.splitlines() if "Connected network" in line), None)
    state = "connected" if ssid else "disconnected"
    print(json.dumps({
        "connected": state == "connected",
        "ssid": ssid or "Disconnected",
        "icon": "󰖩" if state == "connected" else "󱛅",
        "label": ssid or "Disconnected"
    }))


except Exception:
    print(json.dumps({"connected": False, "ssid": "Error", "icon": "󰖪", "label": "Disconnected"}))
