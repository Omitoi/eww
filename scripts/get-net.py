#!/usr/bin/env python3
import subprocess
import json

def get_wifi_info():
    try:
        res = subprocess.check_output(["iwctl", "station", "wlan0", "show"], text=True)
        ssid = None
        state = "disconnected"
        for line in res.splitlines():
            line = line.strip()
            if line.startswith("Connected network"):
                ssid = line.split("Connected network", 1)[1].strip()
                state = "connected"
            elif line.startswith("State"):
                current_state = line.split("State", 1)[1].strip()
                if current_state != "connected" and not ssid:
                    state = current_state

        if state == "connected" and ssid:
            icon = "󰤨"
            label = ssid
        else:
            icon = "󰤭"
            label = "Disconnected"

        return json.dumps({
            "connected": state == "connected",
            "ssid": ssid or "Disconnected",
            "icon": icon,
            "label": label
        })
    except Exception as e:
        return json.dumps({
            "connected": False,
            "ssid": "Error",
            "icon": "󰤭",
            "label": "Disconnected"
        })

if __name__ == "__main__":
    print(get_wifi_info())
