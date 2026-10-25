#!/usr/bin/env python3
import glob
import json
import os
import socket
import subprocess
import sys
import time

def find_socket():
    uid = os.getuid()
    runtime_dir = os.environ.get("XDG_RUNTIME_DIR", f"/run/user/{uid}")
    sig = os.environ.get("HYPRLAND_INSTANCE_SIGNATURE", "")
    if sig:
        candidate = os.path.join(runtime_dir, "hypr", sig, ".socket2.sock")
        if os.path.exists(candidate):
            return candidate
    socks = glob.glob(f"{runtime_dir}/hypr/*/.socket2.sock")
    if socks:
        detected_sig = socks[0].split(os.sep)[-2]
        os.environ["HYPRLAND_INSTANCE_SIGNATURE"] = detected_sig
        return socks[0]
    return None

def wait_for_eww(max_attempts=75):
    for _ in range(max_attempts):
        res = subprocess.run(["eww", "ping"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if res.returncode == 0:
            return True
        time.sleep(0.2)
    return False

def get_hypr_monitors():
    try:
        out = subprocess.check_output(["hyprctl", "monitors", "-j"], text=True)
        mons = json.loads(out)
        return [m["id"] for m in mons if "id" in m]
    except Exception:
        return []

def get_active_eww_windows():
    try:
        out = subprocess.check_output(["eww", "active-windows"], text=True)
        windows = set()
        for line in out.splitlines():
            if ":" in line:
                win_name = line.split(":", 1)[1].strip()
                windows.add(win_name)
        return windows
    except Exception:
        return set()

def sync_monitors():
    mon_ids = set(get_hypr_monitors())
    active_wins = get_active_eww_windows()

    for mid in sorted(mon_ids):
        bar_win = f"bar_{mid}"
        splash_win = f"verse_splash_{mid}"

        if bar_win not in active_wins:
            subprocess.run(
                ["eww", "--no-daemonize", "open", bar_win],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        if splash_win not in active_wins:
            subprocess.run(
                ["eww", "--no-daemonize", "open", splash_win],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

    for win in list(active_wins):
        for prefix in ("bar_", "verse_splash_"):
            if win.startswith(prefix):
                try:
                    mid = int(win[len(prefix):])
                    if mid not in mon_ids:
                        subprocess.run(
                            ["eww", "--no-daemonize", "close", win],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                except ValueError:
                    pass

def main():
    if not wait_for_eww():
        sys.exit(1)

    find_socket()
    sync_monitors()

    while True:
        sock_path = find_socket()
        if not sock_path:
            time.sleep(2)
            continue
        try:
            s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            s.connect(sock_path)
            buf = ""
            while True:
                data = s.recv(4096)
                if not data:
                    break
                buf += data.decode("utf-8", errors="ignore")
                while "\n" in buf:
                    line, buf = buf.split("\n", 1)
                    line = line.strip()
                    if not line:
                        continue
                    event_type = line.split(">>")[0]
                    if event_type in ("monitoradded", "monitoraddedv2", "monitorremoved", "monitorremovedv2"):
                        time.sleep(0.3)
                        sync_monitors()
        except Exception:
            time.sleep(1)

if __name__ == "__main__":
    main()
