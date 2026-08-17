#!/usr/bin/env python3
import json
import subprocess

def toggle_wifi():
    try:
        monitors = json.loads(subprocess.check_output(["hyprctl", "monitors", "-j"], text=True))
        focused_mon = 0
        for mon in monitors:
            if mon.get("focused", False):
                focused_mon = mon.get("id", 0)
                break
        
        # Check active windows in eww
        active_windows = subprocess.check_output(["eww", "active-windows"], text=True)
        is_open = any(w.startswith("wifi_window_") for w in active_windows.splitlines())

        if is_open:
            subprocess.run(["eww", "close", f"wifi_window_{focused_mon}"], stderr=subprocess.DEVNULL)
            # Close all wifi windows just in case
            subprocess.run(["eww", "close", "wifi_window_0", "wifi_window_1"], stderr=subprocess.DEVNULL)
        else:
            subprocess.run(["eww", "open", f"wifi_window_{focused_mon}"])
    except Exception as e:
        subprocess.run(["eww", "open", "wifi_window_0"])

if __name__ == "__main__":
    toggle_wifi()
