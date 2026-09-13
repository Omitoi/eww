#!/usr/bin/env python3
import os
import sys
import json
import time
import socket
import subprocess

LOCK_FILE = "/tmp/eww_kb_osd.lock"

LAYOUT_MAP = [
    ("czech", "CZ", "Czech"),
    ("english", "US", "English"),
    ("russian", "RU", "Russian"),
    ("norwegian", "NO", "Norwegian"),
]

def parse_layout(keymap_str):
    k = (keymap_str or "").lower()
    for pattern, code, name in LAYOUT_MAP:
        if pattern in k:
            return {"code": code, "name": name}
    # Fallback to first 2 characters uppercased
    code = (keymap_str[:2] if keymap_str else "??").upper()
    return {"code": code, "name": keymap_str or "Unknown"}

def get_current_layout():
    try:
        out = subprocess.check_output(["hyprctl", "devices", "-j"], text=True)
        devs = json.loads(out)
        kb = next((k for k in devs.get("keyboards", []) if k.get("main")), None)
        if not kb and devs.get("keyboards"):
            kb = devs["keyboards"][0]
        keymap = kb.get("active_keymap", "Czech") if kb else "Czech"
        return parse_layout(keymap)
    except Exception:
        return {"code": "CZ", "name": "Czech"}

def get_focused_monitor():
    try:
        mons = json.loads(subprocess.check_output(["hyprctl", "monitors", "-j"], text=True))
        focused = next((m for m in mons if m.get("focused")), mons[0])
        return focused.get("id", 0)
    except Exception:
        return 0

def show_osd():
    try:
        mon_id = get_focused_monitor()
        subprocess.run(["eww", "open", f"kb_osd_window_{mon_id}"], stderr=subprocess.DEVNULL)
        
        cur_time = time.time()
        with open(LOCK_FILE, "w") as f:
            f.write(str(cur_time))
            
        if os.fork() == 0:
            time.sleep(1.0)
            try:
                with open(LOCK_FILE, "r") as f:
                    last_time = float(f.read().strip())
                if time.time() - last_time >= 0.95:
                    subprocess.run(["eww", "close", "kb_osd_window_0", "kb_osd_window_1"], stderr=subprocess.DEVNULL)
            except Exception:
                pass
            os._exit(0)
    except Exception:
        pass

def main():
    # Emit initial state immediately for EWW deflisten
    current = get_current_layout()
    print(json.dumps(current), flush=True)

    runtime = os.environ.get("XDG_RUNTIME_DIR", f"/run/user/{os.getuid()}")
    sig = os.environ.get("HYPRLAND_INSTANCE_SIGNATURE", "")
    sock_path = os.path.join(runtime, "hypr", sig, ".socket2.sock")

    while True:
        if not os.path.exists(sock_path):
            time.sleep(1)
            continue
        try:
            s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            s.connect(sock_path)
            buf = ""
            while True:
                data = s.recv(4096).decode("utf-8", errors="ignore")
                if not data:
                    break
                buf += data
                while "\n" in buf:
                    line, buf = buf.split("\n", 1)
                    line = line.strip()
                    if line.startswith("activelayout>>"):
                        parts = line.split(">>", 1)[1].split(",", 1)
                        if len(parts) > 1:
                            layout_str = parts[1].strip()
                            parsed = parse_layout(layout_str)
                            print(json.dumps(parsed), flush=True)
                            show_osd()
        except Exception:
            time.sleep(1)

if __name__ == "__main__":
    main()
