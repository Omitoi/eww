#!/usr/bin/env python3
import json, subprocess

try:
    cx, cy = map(int, subprocess.check_output(["hyprctl", "cursorpos"], text=True).strip().split(","))
    mons = json.loads(subprocess.check_output(["hyprctl", "monitors", "-j"], text=True))
    m = next((m for m in mons if m["x"] <= cx < m["x"] + m["width"] and m["y"] <= cy < m["y"] + m["height"]), mons[0])
    mon_id = m["id"]
except Exception:
    mon_id = 0

window_name = f"power_window_{mon_id}"
subprocess.run(["eww", "open", "--toggle", window_name])
