#!/usr/bin/env python3
import sys
import json
import subprocess

try:
    monitors = json.loads(subprocess.check_output(["hyprctl", "monitors", "-j"], text=True))
    focused_mon = next((m for m in monitors if m.get("focused")), monitors[0])
    mon_id = focused_mon["id"]
except Exception:
    mon_id = 0

window_name = f"volume_window_{mon_id}"
subprocess.run(["eww", "open", "--toggle", window_name])
