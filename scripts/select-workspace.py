#!/usr/bin/env python3
import sys
import json
import subprocess

if len(sys.argv) < 3:
    sys.exit(1)

target_ws = int(sys.argv[1])
click_mon = int(sys.argv[2])

try:
    mons = json.loads(subprocess.check_output(["hyprctl", "monitors", "-j"], text=True))
    wss = json.loads(subprocess.check_output(["hyprctl", "workspaces", "-j"], text=True))

    click_mon_data = next((m for m in mons if m["id"] == click_mon), None)
    if not click_mon_data:
        sys.exit(0)

    click_mon_active_ws = click_mon_data["activeWorkspace"]["id"]
    if target_ws == click_mon_active_ws:
        sys.exit(0)

    target_ws_data = next((w for w in wss if w["id"] == target_ws), None)
    other_mon = next((m for m in mons if m["id"] != click_mon and m["activeWorkspace"]["id"] == target_ws), None)

    if other_mon:
        # Only swap if target workspace is actively displayed on the other monitor
        other_mon_id = other_mon["id"]
        subprocess.run(["hyprctl", "eval", f"hl.dispatch(hl.dsp.workspace.move({{ workspace = {target_ws}, monitor = {click_mon} }}))"])
        subprocess.run(["hyprctl", "eval", f"hl.dispatch(hl.dsp.workspace.move({{ workspace = {click_mon_active_ws}, monitor = {other_mon_id} }}))"])
        subprocess.run(["hyprctl", "eval", f"hl.dispatch(hl.dsp.focus({{ workspace = {target_ws} }}))"])
    else:
        # Otherwise, switch only the clicked monitor; leave other monitor untouched
        if target_ws_data and target_ws_data["monitorID"] != click_mon:
            subprocess.run(["hyprctl", "eval", f"hl.dispatch(hl.dsp.workspace.move({{ workspace = {target_ws}, monitor = {click_mon} }}))"])
        subprocess.run(["hyprctl", "eval", f"hl.dispatch(hl.dsp.focus({{ workspace = {target_ws} }}))"])

except Exception:
    pass
