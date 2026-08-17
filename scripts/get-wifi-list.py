#!/usr/bin/env python3
import subprocess
import json
import re

def get_networks():
    try:
        # Strip ANSI escape sequences
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        
        # Fetch cached networks without blocking on active radio scan
        out = subprocess.check_output(["iwctl", "station", "wlan0", "get-networks"], text=True)

        networks = []
        
        for line in out.splitlines():
            clean = ansi_escape.sub('', line)
            if "Network name" in clean or "---" in clean or "Available networks" in clean or not clean.strip():
                continue
            
            is_connected = ">" in clean[:8]
            clean_name_line = clean.replace(">", " ").strip()
            
            # The columns are formatted around fixed column widths or 2+ spaces
            # Network name is usually first 32 chars
            name = clean_name_line[:32].strip()
            rest = clean_name_line[32:].strip()
            parts = rest.split()
            security = parts[0] if parts else ""
            signal = parts[1] if len(parts) > 1 else ""

            if name:
                networks.append({
                    "name": name,
                    "security": security,
                    "signal": signal,
                    "connected": is_connected
                })
        return json.dumps(networks)
    except Exception as e:
        return json.dumps([])

if __name__ == "__main__":
    print(get_networks())
