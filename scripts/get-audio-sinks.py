#!/usr/bin/env python3
import json, subprocess

sinks = []
try:
    lines = subprocess.check_output(["wpctl", "status"], text=True).splitlines()
    in_sinks = False
    for line in lines:
        if "Sinks:" in line: in_sinks = True; continue
        elif in_sinks and ("Sources:" in line or "Filters:" in line or "Streams:" in line): break
        if in_sinks and line.strip():
            parts = line.replace("│", "").replace("*", "").strip().split(".", 1)
            if len(parts) == 2:
                sinks.append({"id": parts[0].strip(), "name": parts[1].split("[vol:")[0].strip(), "default": "*" in line})
except Exception: pass

print(json.dumps(sinks))
