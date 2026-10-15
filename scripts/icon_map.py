#!/usr/bin/env python3
"""
Nerd Font icon mapping for installed desktop applications.
"""

ICON_MAP = {
    "kitty": "󰿠",
    "thunar": "󰉋",
    "hyprlauncher": "󰀻",
    "rofi": "󰀻",
    "steam": "󰓓",
    "pavucontrol": "󰕾",
    "obsidian": "󰏫",
    "firefox": "󰈹",
    "brave": "",
    "google-chrome": "󰊯",
    "code": "󰨞",
    "neovim": "󰅩",
    "discord": "󰙯",
    "spotify": "󰓇",
    "vlc": "󰕼",
}

def resolve_icon(app_class, app_title):
    cls = (app_class or "").lower()
    ttl = (app_title or "").lower()

    if cls in ICON_MAP:
        return ICON_MAP[cls]

    for key, icon in ICON_MAP.items():
        if key in cls or key in ttl:
            return icon

    if any(k in cls or k in ttl for k in ["term", "console", "shell"]): return "󰆍"
    if any(k in cls or k in ttl for k in ["browser", "web"]): return "󰈹"
    if any(k in cls or k in ttl for k in ["edit", "code", "dev"]): return "󰅩"
    if any(k in cls or k in ttl for k in ["file", "fm", "archive"]): return "󰉋"
    if any(k in cls or k in ttl for k in ["audio", "sound", "music"]): return "󰓇"
    if any(k in cls or k in ttl for k in ["video", "media"]): return "󰕼"

    return "󰌽"
