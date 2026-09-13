#!/usr/bin/env python3
import os
import glob
import json

def get_battery():
    bats = []
    # Search for all battery devices in /sys/class/power_supply/
    for path in sorted(glob.glob("/sys/class/power_supply/*")):
        type_file = os.path.join(path, "type")
        if os.path.isfile(type_file):
            try:
                with open(type_file, "r") as f:
                    if f.read().strip() == "Battery":
                        # If present file exists and indicates absent, skip
                        pres_file = os.path.join(path, "present")
                        if os.path.isfile(pres_file):
                            with open(pres_file, "r") as pf:
                                if pf.read().strip() == "0":
                                    continue
                        bats.append(path)
            except Exception:
                pass

    if not bats:
        return {
            "has_battery": False,
            "capacity": 0,
            "status": "No battery",
            "icon": "󰁹",
            "label": ""
        }

    total_energy_now = 0
    total_energy_full = 0
    total_cap = 0
    cap_count = 0
    statuses = []

    for b in bats:
        # Read status
        status = "Unknown"
        status_file = os.path.join(b, "status")
        if os.path.isfile(status_file):
            try:
                with open(status_file, "r") as sf:
                    status = sf.read().strip()
            except Exception:
                pass
        statuses.append(status)

        # Read capacity
        cap_file = os.path.join(b, "capacity")
        if os.path.isfile(cap_file):
            try:
                with open(cap_file, "r") as cf:
                    c = int(cf.read().strip())
                    total_cap += c
                    cap_count += 1
            except Exception:
                pass

        # Also check energy / charge to compute accurate composite percentage if multi-battery
        en_now = None
        for en_name in ["energy_now", "charge_now"]:
            p = os.path.join(b, en_name)
            if os.path.isfile(p):
                try:
                    with open(p, "r") as ef:
                        en_now = int(ef.read().strip())
                        break
                except Exception:
                    pass

        en_full = None
        for en_name in ["energy_full", "charge_full"]:
            p = os.path.join(b, en_name)
            if os.path.isfile(p):
                try:
                    with open(p, "r") as ef:
                        en_full = int(ef.read().strip())
                        break
                except Exception:
                    pass

        if en_now is not None and en_full is not None and en_full > 0:
            total_energy_now += en_now
            total_energy_full += en_full

    if total_energy_full > 0:
        capacity = max(0, min(100, int(round((total_energy_now / total_energy_full) * 100))))
    elif cap_count > 0:
        capacity = max(0, min(100, int(round(total_cap / cap_count))))
    else:
        capacity = 0

    if any(s == "Charging" for s in statuses):
        main_status = "Charging"
    elif all(s == "Full" for s in statuses):
        main_status = "Full"
    elif any(s == "Discharging" for s in statuses):
        main_status = "Discharging"
    else:
        main_status = statuses[0] if statuses else "Unknown"

    icon = "󰂄" if main_status in ["Charging", "Full"] else "󰁹"
    pad = "  " if capacity < 10 else (" " if capacity < 100 else "")
    label = f"{icon} {pad}{capacity}%"

    return {
        "has_battery": True,
        "capacity": capacity,
        "status": main_status,
        "icon": icon,
        "label": label
    }

if __name__ == "__main__":
    print(json.dumps(get_battery()))
