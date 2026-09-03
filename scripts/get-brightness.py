#!/usr/bin/env python3
import os, glob

def get_brightness_raw():
    backlights = glob.glob("/sys/class/backlight/*")
    if not backlights:
        return 100, "󰃠", "󰃠 100%"
    path = backlights[0]
    try:
        with open(os.path.join(path, "brightness"), "r") as f:
            b = int(f.read().strip())
        with open(os.path.join(path, "max_brightness"), "r") as f:
            max_b = int(f.read().strip())
        perc = max(0, min(100, int(round((b / max_b) * 100))))
        icon = "󰃠" if perc >= 60 else ("󰃝" if perc >= 30 else "󰃞")
        pad = "  " if perc < 10 else (" " if perc < 100 else "")
        return perc, icon, f"{icon} {pad}{perc}%"
    except Exception:
        return 100, "󰃠", "󰃠 100%"

if __name__ == "__main__":
    _, _, bar_text = get_brightness_raw()
    print(bar_text)
