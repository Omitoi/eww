#!/usr/bin/env python3
import json, glob, os

def get_battery():
    bats = glob.glob("/sys/class/power_supply/BAT*")
    if not bats:
        return {"has_battery": False, "capacity": 0, "status": "No battery", "icon": "󰁹", "label": ""}

    bat = bats[0]
    try:
        with open(os.path.join(bat, "capacity")) as f:
            cap = int(f.read().strip())
        with open(os.path.join(bat, "status")) as f:
            status = f.read().strip()
    except Exception:
        return {"has_battery": False, "capacity": 0, "status": "Unknown", "icon": "󰁹", "label": ""}

    icon = "󰂄" if status in ["Charging", "Full"] else "󰁹"
    pad = "  " if cap < 10 else (" " if cap < 100 else "")
    return {"has_battery": True, "capacity": cap, "status": status, "icon": icon, "label": f"{icon} {pad}{cap}%"}

if __name__ == "__main__":
    print(json.dumps(get_battery()))
