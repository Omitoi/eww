#!/usr/bin/env python3
import json, os, socket, subprocess, sys

ICON_MAP = {"kitty": "󰆍", "foot": "󰆍", "Alacritty": "󰆍", "firefox": "󰈹", "chromium": "󰈹", "Brave-browser": "󰈹", "Code": "󰨞", "thunar": "󰉋", "Nemo": "󰉋", "spotify": "󰓇", "discord": "󰙯"}

def get_hypr(cmd):
    return json.loads(subprocess.check_output(["hyprctl", cmd, "-j"], text=True))

def print_state(target_mon):
    monitors, workspaces, clients = get_hypr("monitors"), get_hypr("workspaces"), get_hypr("clients")
    active_ws = next((m["activeWorkspace"]["id"] for m in monitors if m["id"] == target_mon), 1)
    all_ids = set(w["id"] for w in workspaces if w["id"] > 0) | {active_ws}
    max_ws = max(all_ids) if all_ids else 1
    
    ws_list, active_wins = [], []
    for ws_id in range(1, max_ws + 1):
        ws_clients = [c for c in clients if c["workspace"]["id"] == ws_id]
        # In Hyprland Master layout, the client with smallest x (and top y) or first client is master
        master_addr = min(ws_clients, key=lambda c: (c["at"][0], c["at"][1]))["address"] if ws_clients else None
        
        wins = [
            {
                "address": c["address"],
                "title": c["title"],
                "icon": ICON_MAP.get(c.get("class", ""), "󰌽"),
                "is_master": c["address"] == master_addr
            }
            for c in ws_clients
        ]
        if ws_id == active_ws:
            active_wins.extend(wins)
        ws_list.append({"id": ws_id, "label": f"{ws_id} {' '.join(w['icon'] for w in wins)}".strip() if wins else str(ws_id), "windows": wins})

    print(json.dumps({"active": active_ws, "next_ws": max_ws + 1, "workspaces": ws_list, "active_windows": active_wins}), flush=True)

if __name__ == "__main__":
    target_mon = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    print_state(target_mon)
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(f"{os.environ.get('XDG_RUNTIME_DIR', '/tmp')}/hypr/{os.environ.get('HYPRLAND_INSTANCE_SIGNATURE')}/.socket2.sock")
    while True:
        data = sock.recv(4096).decode('utf-8')
        if not data: break
        if any(e in data for e in ["workspace>>", "focusedmon>>", "openwindow>>", "closewindow>>", "movewindow>>", "createworkspace>>", "destroyworkspace>>"]):
            print_state(target_mon)