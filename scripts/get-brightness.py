#!/usr/bin/env python3
import subprocess

try:
    b = int(subprocess.check_output(["brightnessctl", "-m"]).decode().split(",")[3].rstrip("%\n"))
    icon = "󰃠" if b >= 60 else ("󰃝" if b >= 30 else "󰃞")
    pad = "  " if b < 10 else (" " if b < 100 else "")
    print(f"{icon} {pad}{b}%")
except Exception:
    print("")
