#!/usr/bin/env python3
import subprocess
import json
import time

def get_bt_list():
    try:
        out = subprocess.check_output(["bluetoothctl", "devices"], text=True)
        conn_out = subprocess.check_output(["bluetoothctl", "devices", "Connected"], text=True)
        conn_macs = set(line.split()[1] for line in conn_out.splitlines() if len(line.split()) > 1)
        
        devs = [
            {"mac": parts[1], "name": parts[2], "connected": parts[1] in conn_macs}
            for line in out.splitlines()
            if len(parts := line.strip().split(" ", 2)) >= 3
        ]

        if not devs:
            # Trigger active scan in background if no devices found
            subprocess.Popen(["bluetoothctl", "--timeout", "5", "scan", "on"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return json.dumps({
                "empty": True,
                "devices": [],
                "message": "No devices found\nscanning..."
            })

        return json.dumps({
            "empty": False,
            "devices": devs,
            "message": ""
        })
    except Exception:
        return json.dumps({
            "empty": True,
            "devices": [],
            "message": "No devices found\nscanning..."
        })

if __name__ == "__main__":
    print(get_bt_list())
