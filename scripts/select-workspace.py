#!/usr/bin/env python3
import sys
import json
import subprocess

if len(sys.argv) < 3:
    sys.exit(1)

target_ws = int(sys.argv[1])


click_mon = int(sys.argv[2])

try:
    monitors = json.loads(subprocess.check_output(["hyprctl", "monitors", "-j"], text=True))
    workspaces = json.loads(subprocess.check_output(["hyprctl", "workspaces", "-j"], text=True))

    target_ws_data = next((w for w in workspaces if w["id"] == target_ws), None)
    click_mon_data = next((m for m in monitors if m["id"] == click_mon), None)

    if target_ws_data and click_mon_data:
        target_current_mon = target_ws_data["monitorID"]
        click_mon_active_ws = click_mon_data["activeWorkspace"]["id"]

        if target_current_mon == click_mon:
            # Workspace on clicked monitor -> focus it
            subprocess.run(["hyprctl", "eval", f"hl.dispatch(hl.dsp.focus({{ workspace = {target_ws} }}))"])
        else:
            # Swap workspace monitors
            subprocess.run(["hyprctl", "eval", f"hl.dispatch(hl.dsp.workspace.move({{ workspace = {target_ws}, monitor = {click_mon} }}))"])
            subprocess.run(["hyprctl", "eval", f"hl.dispatch(hl.dsp.workspace.move({{ workspace = {click_mon_active_ws}, monitor = {target_current_mon} }}))"])
            subprocess.run(["hyprctl", "eval", f"hl.dispatch(hl.dsp.focus({{ workspace = {target_ws} }}))"])
    else:
        # Create/focus new workspace on target monitor
        subprocess.run(["hyprctl", "eval", f"hl.dispatch(hl.dsp.focus({{ workspace = {target_ws} }}))"])

except Exception as e:
    subprocess.run(["hyprctl", "eval", f"hl.dispatch(hl.dsp.focus({{ workspace = {target_ws} }}))"])
