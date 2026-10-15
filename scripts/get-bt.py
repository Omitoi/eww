#!/usr/bin/env python3
import glob
import json
import os
import subprocess

def get_bt_status():
    if not os.path.exists("/sys/class/bluetooth") or not glob.glob("/sys/class/bluetooth/hci*"):
        return {
            "has_bluetooth": False,
            "connected": False,
            "powered": False,
            "label": "",
            "icon": "",
            "devices": []
        }

    try:
        powered = False
        res = subprocess.check_output(["bluetoothctl", "show"], text=True, timeout=2)
        for line in res.splitlines():
            if "Powered: yes" in line:
                powered = True
                break

        conn_out = subprocess.check_output(["bluetoothctl", "devices", "Connected"], text=True, timeout=2)
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

        return {
            "has_bluetooth": True,
            "connected": connected,
            "powered": powered,
            "label": label,
            "icon": icon,
            "devices": connected_devs
        }
    except Exception:
        return {
            "has_bluetooth": True,
            "connected": False,
            "powered": False,
            "label": "Disabled",
            "icon": "󰂲",
            "devices": []
        }

if __name__ == "__main__":
    print(json.dumps(get_bt_status()))
