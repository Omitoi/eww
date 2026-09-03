#!/usr/bin/env python3
import sys, json, subprocess

def toggle_verse():
    try:
        # Check current verse text from EWW
        curr = subprocess.check_output(["eww", "get", "daily_verse"], text=True).strip()
    except Exception:
        curr = ""

    if not curr or "Unable to fetch" in curr or "Error" in curr or "Connecting" in curr:
        # Retry fetching verse immediately
        try:
            res = subprocess.check_output(["python3", "/home/omitoi/.config/eww/scripts/get-verse.py"], text=True).strip()
            subprocess.run(["eww", "update", f"daily_verse={res}"])
        except Exception:
            pass
    else:
        # If verse is fetched successfully, toggle popup window on focused monitor
        try:
            cx, cy = map(int, subprocess.check_output(["hyprctl", "cursorpos"], text=True).strip().split(","))
            mons = json.loads(subprocess.check_output(["hyprctl", "monitors", "-j"], text=True))
            m = next((m for m in mons if m["x"] <= cx < m["x"] + m["width"] and m["y"] <= cy < m["y"] + m["height"]), mons[0])
            mon_id = m["id"]
        except Exception:
            mon_id = 0

        subprocess.run(["eww", "open", "--toggle", f"verse_window_{mon_id}"])

if __name__ == "__main__":
    toggle_verse()
