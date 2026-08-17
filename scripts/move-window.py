#!/usr/bin/env python3
import sys, subprocess
if len(sys.argv) > 2:
    subprocess.run(["hyprctl", "eval", f"hl.dispatch(hl.dsp.window.move({{ window = 'address:{sys.argv[1]}', workspace = {sys.argv[2]} }}))"])
