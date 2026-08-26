#!/usr/bin/env python3
import subprocess
import json

def get_bt_list():
    try:
        out = subprocess.check_output(["bluetoothctl", "devices"], text=True)
        conn_out = subprocess.check_output(["bluetoothctl", "devices", "Connected"], text=True)
        conn_macs = set(line.split()[1] for line in conn_out.splitlines() if len(line.split()) > 1)
        
        devs = []
        for line in out.splitlines():
            parts = line.strip().split(" ", 2)
            if len(parts) >= 3:
                mac, name = parts[1], parts[2]
                devs.append({
                    "mac": mac,
                    "name": name,
                    "connected": mac in conn_macs
                })
        print(json.dumps(devs))
    except Exception:
        print(json.dumps([]))

if __name__ == "__main__":
    get_bt_list()
