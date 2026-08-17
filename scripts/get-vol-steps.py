#!/usr/bin/env python3
import json, sys

try:
    curr = 0 if sys.argv[1] == "MUTED" else int(sys.argv[1])
except Exception:
    curr = 0

steps = list(range(0, 105, 5))
res = [
    {
        "val": s,
        "label": f"{s}%" if s == curr else ("00" if s == 100 else str(s)),
        "selected": s == curr,
        "scale": "active" if s == curr else ("adj" if abs(s - curr) == 5 else "dim")
    }
    for s in steps
]
print(json.dumps(res))
