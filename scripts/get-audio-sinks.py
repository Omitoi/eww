#!/usr/bin/env python3
import json
import subprocess

def get_audio_sinks():
    try:
        output = subprocess.check_output(["wpctl", "status"], text=True)
        lines = output.splitlines()
        
        sinks = []
        in_sinks = False
        
        for line in lines:
            if "Sinks:" in line:
                in_sinks = True
                continue
            elif in_sinks and ("Sources:" in line or "Filters:" in line or "Streams:" in line):
                in_sinks = False
                break
                
            if in_sinks and line.strip():
                # Extract sink ID, name, and default state
                # Format example: "│ *   53. Kraken Tournament Edition Chat      [vol: 0.86]"
                is_default = "*" in line
                clean = line.replace("│", "").replace("*", "").strip()
                parts = clean.split(".", 1)
                if len(parts) == 2:
                    sink_id = parts[0].strip()
                    name_part = parts[1].split("[vol:")[0].strip()
                    sinks.append({
                        "id": sink_id,
                        "name": name_part,
                        "default": is_default
                    })
        return sinks
    except Exception:
        return []

if __name__ == "__main__":
    print(json.dumps(get_audio_sinks()))
