#!/usr/bin/env python3
import json, subprocess

def get_net_status():
    try:
        route = subprocess.check_output(["ip", "route", "get", "1.1.1.1"], text=True)
        tokens = route.split()
        dev = next((tokens[i+1] for i in range(len(tokens)-1) if tokens[i] == "dev"), None)
        if not dev:
            return {"connected": False, "ssid": "Disconnected", "icon": "󱛅", "label": "Disconnected"}

        if dev.startswith("wl"):
            res = subprocess.check_output(["iwctl", "station", dev, "show"], text=True)
            ssid = next((line.split("Connected network", 1)[1].strip() for line in res.splitlines() if "Connected network" in line), None)
            return {
                "connected": bool(ssid),
                "ssid": ssid or "Disconnected",
                "icon": "󰖩" if ssid else "󱛅",
                "label": ssid or "Disconnected"
            }
        else:
            return {
                "connected": True,
                "ssid": "Ethernet",
                "icon": "󰈀",
                "label": "Ethernet"
            }
    except Exception:
        return {"connected": False, "ssid": "Disconnected", "icon": "󰖪", "label": "Disconnected"}

if __name__ == "__main__":
    print(json.dumps(get_net_status()))
