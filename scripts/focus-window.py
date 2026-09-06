#!/usr/bin/env python3
import sys, json, subprocess

if len(sys.argv) > 1:
    target_addr = sys.argv[1]
    
    if target_addr.startswith("launch:"):


        cmd = target_addr.split("launch:")[1]
        subprocess.Popen([cmd])
        sys.exit(0)

    
    try:
        clients = json.loads(subprocess.check_output(["hyprctl", "clients", "-j"], text=True))
        monitors = json.loads(subprocess.check_output(["hyprctl", "monitors", "-j"], text=True))
        
        target = next((c for c in clients if c["address"] == target_addr), None)
        if target:
            target_ws = target["workspace"]["id"]
            ws_clients = [c for c in clients if c["workspace"]["id"] == target_ws]
            
            # Master window is the client positioned at the left (smallest x coordinate)
            master_c = min(ws_clients, key=lambda c: (c["at"][0], c["at"][1])) if ws_clients else None
            
            # Focus target window first
            subprocess.run(["hyprctl", "eval", f"hl.dispatch(hl.dsp.focus({{ window = 'address:{target_addr}' }}))"])
            
            # Only swap if the target is NOT already master
            if master_c and master_c["address"] != target_addr:
                subprocess.run(["hyprctl", "eval", "hl.dispatch(hl.dsp.layout('swapwithmaster master'))"])
    except Exception:
        subprocess.run(["hyprctl", "eval", f"hl.dispatch(hl.dsp.focus({{ window = 'address:{target_addr}' }}))"])
