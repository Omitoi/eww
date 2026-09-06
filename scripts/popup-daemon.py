#!/usr/bin/env python3
import os, glob, socket, subprocess, sys, time

POPUP_WINDOWS = {
    "calendar_window_0", "calendar_window_1",
    "power_window_0", "power_window_1",
    "volume_window_0", "volume_window_1",
    "wifi_window_0", "wifi_window_1",
    "bt_window_0", "bt_window_1",
}

def get_active_popups():
    try:
        out = subprocess.check_output(["eww", "active-windows"], text=True)
        active = {line.split(":")[0].strip() for line in out.splitlines() if ":" in line}
        return list(active & POPUP_WINDOWS)
    except Exception:
        return []

def close_popups(popups):
    if popups:
        subprocess.run(["eww", "close"] + popups, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def find_socket():
    uid = os.getuid()
    socks = glob.glob(f"/run/user/{uid}/hypr/*/.socket2.sock")
    if socks:
        return socks[0]
    runtime_dir = os.environ.get("XDG_RUNTIME_DIR", f"/run/user/{uid}")
    sig = os.environ.get("HYPRLAND_INSTANCE_SIGNATURE", "")
    if sig:
        candidate = os.path.join(runtime_dir, "hypr", sig, ".socket2.sock")
        if os.path.exists(candidate):
            return candidate
    return None

def main():
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
                    # When focus changes to any window or workspace, dismiss open popups
                    if event_type in ("activewindow", "activewindowv2", "workspace", "workspacev2", "focusedmon"):
                        popups = get_active_popups()
                        if popups:
                            close_popups(popups)
        except Exception:
            time.sleep(1)

if __name__ == "__main__":
    main()
