#!/usr/bin/env python3
import json, subprocess

def get_bt_status():
    try:
        powered = False
        res = subprocess.check_output(["bluetoothctl", "show"], text=True)
        for line in res.splitlines():
            if "Powered: yes" in line:
                powered = True
                break

        conn_out = subprocess.check_output(["bluetoothctl", "devices", "Connected"], text=True)
        connected_devs = []
        for line in conn_out.splitlines():
            parts = line.strip().split(" ", 2)
            if len(parts) >= 3:
                connected_devs.append({"mac": parts[1], "name": parts[2]})

        if not powered:
            icon = "󰂲"
            label = "Disabled"
            connected = False
        elif connected_devs:
            icon = "󰂱"
            label = connected_devs[0]["name"]
            connected = True
        else:
            icon = "󰂯"
            label = "On"
            connected = True

        print(json.dumps({
            "connected": connected,
            "powered": powered,
            "label": label,
            "icon": icon,
            "devices": connected_devs
        }))
    except Exception:
        print(json.dumps({"connected": False, "powered": False, "label": "Disabled", "icon": "󰂲", "devices": []}))

if __name__ == "__main__":
    get_bt_status()
