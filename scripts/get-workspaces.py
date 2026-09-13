#!/usr/bin/env python3
import json, os, socket, subprocess, sys
from icon_map import resolve_icon

def get_hypr(cmd):
    return json.loads(subprocess.check_output(["hyprctl", cmd, "-j"], text=True))

def print_state(target_mon):
    monitors, workspaces, clients = get_hypr("monitors"), get_hypr("workspaces"), get_hypr("clients")
    active_ws = next((m["activeWorkspace"]["id"] for m in monitors if m["id"] == target_mon), 1)
    all_ids = set(w["id"] for w in workspaces if w["id"] > 0) | {active_ws}
    max_ws = max(all_ids) if all_ids else 1
    
    ws_list, active_wins = [], []
    all_client_addrs = set()

    for ws_id in range(1, max_ws + 1):
        ws_clients = [c for c in clients if c["workspace"]["id"] == ws_id]
        master_addr = min(ws_clients, key=lambda c: (c["at"][0], c["at"][1]))["address"] if ws_clients else None
        
        wins = []
        for c in ws_clients:
            all_client_addrs.add(c["address"])
            wins.append({
                "address": c["address"],
                "title": c["title"],
                "icon": resolve_icon(c.get("class", ""), c.get("title", "")),
                "is_master": c["address"] == master_addr
            })
        
        if ws_id == active_ws:
            active_wins.extend(wins)
        ws_list.append({"id": ws_id, "label": f"{ws_id} {' '.join(w['icon'] for w in wins)}".strip() if wins else str(ws_id), "windows": wins})

    # Background / unmapped / hidden apps running anywhere across Hyprland
    bg_wins = []
    registered_classes = set(c.get("class", "").lower() for c in clients)

    for c in clients:
        if c["address"] not in all_client_addrs or c.get("hidden", False) or not c.get("mapped", True):
            bg_wins.append({
                "address": c["address"],
                "title": c["title"],
                "icon": resolve_icon(c.get("class", ""), c.get("title", ""))
            })

    print(json.dumps({
        "active": active_ws, 
        "next_ws": max_ws + 1, 
        "workspaces": ws_list, 
        "active_windows": active_wins,
        "background_windows": bg_wins
    }), flush=True)


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