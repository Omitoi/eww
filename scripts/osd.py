#!/usr/bin/env python3
import sys, os, time, json, subprocess, importlib.util

_script_dir = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("get_brightness", os.path.join(_script_dir, "get-brightness.py"))
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
get_brightness_raw = _mod.get_brightness_raw

LOCK_FILE = "/tmp/eww_osd_timestamp.lock"

def get_volume_info():
    try:
        out = subprocess.check_output("wpctl get-volume @DEFAULT_AUDIO_SINK@", shell=True, text=True).strip()
        is_muted = "[MUTED]" in out
        parts = out.split()
        vol = float(parts[1]) if len(parts) > 1 else 0.0
        perc = max(0, min(100, int(round(vol * 100))))
        if is_muted:
            return 0, "󰝟", "Muted", "MUTED"
        icon = "󰕾" if perc >= 50 else ("󰖀" if perc > 0 else "󰕿")
        return perc, icon, f"{perc}%", str(perc)
    except Exception:
        return 50, "󰕾", "50%", "50"

def get_focused_monitor():
    try:
        mons = json.loads(subprocess.check_output(["hyprctl", "monitors", "-j"], text=True))
        focused = next((m for m in mons if m.get("focused")), mons[0])
        return focused.get("id", 0)
    except Exception:
        return 0

def handle_action():
    if len(sys.argv) < 3:
        return

    mode, action = sys.argv[1], sys.argv[2] # "brightness" / "volume", "up" / "down" / "mute"

    if mode == "brightness":
        step = "10%+" if action == "up" else "10%-"
        subprocess.run(["brightnessctl", "set", step], stdout=subprocess.DEVNULL)
        val, icon, bar_str = get_brightness_raw()

        label = f"{val}%"
        subprocess.run(["eww", "update", f"brightness={bar_str}", f"osd_icon={icon}", f"osd_value={val}", f"osd_label={label}"])
    elif mode == "volume":
        cmd = ["wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "toggle"] if action == "mute" else ["wpctl", "set-volume", "-l", "1", "@DEFAULT_AUDIO_SINK@", "5%+" if action == "up" else "5%-"]
        subprocess.run(cmd)
        val, icon, label, bar_str = get_volume_info()
        subprocess.run(["eww", "update", f"volume={bar_str}", f"osd_icon={icon}", f"osd_value={val}", f"osd_label={label}"])

    mon_id = get_focused_monitor()
    subprocess.run(["eww", "open", f"osd_window_{mon_id}"])

    # Debounce timer
    cur_time = time.time()
    with open(LOCK_FILE, "w") as f:
        f.write(str(cur_time))

    if os.fork() == 0:
        time.sleep(1.0)
        try:
            with open(LOCK_FILE, "r") as f:
                last_time = float(f.read().strip())
            if time.time() - last_time >= 0.95:
                subprocess.run(["eww", "close", "osd_window_0", "osd_window_1"], stderr=subprocess.DEVNULL)
        except Exception:
            pass
        os._exit(0)

if __name__ == "__main__":
    handle_action()
