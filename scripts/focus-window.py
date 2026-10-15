#!/usr/bin/env python3
import sys, json, subprocess

if len(sys.argv) < 2:
    sys.exit(0)

addr = sys.argv[1]
if addr.startswith("launch:"):
    subprocess.Popen(addr[7:].split())
    sys.exit(0)

subprocess.run(["hyprctl", "eval", f"hl.dispatch(hl.dsp.focus({{ window = 'address:{addr}' }}))"])
try:
    clients = json.loads(subprocess.check_output(["hyprctl", "clients", "-j"], text=True))
    target = next((c for c in clients if c["address"] == addr), None)
    if target:
        ws_clients = [c for c in clients if c["workspace"]["id"] == target["workspace"]["id"]]
        if ws_clients and min(ws_clients, key=lambda c: c["at"][0])["address"] != addr:
            subprocess.run(["hyprctl", "eval", "hl.dispatch(hl.dsp.layout('swapwithmaster master'))"])
except Exception:
    pass
