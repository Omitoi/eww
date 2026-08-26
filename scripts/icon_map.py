#!/usr/bin/env python3
"""
Comprehensive Nerd Font Icon Registry for Linux Desktop Applications.
Maps application classes, binaries, and titles to specific Nerd Font glyphs
with a 3-tier fuzzy resolution fallback engine.
"""

ICON_MAP = {
    # --- Terminals & CLI Shells ---
    "kitty": "󰿠", "foot": "󰆍", "alacritty": "󰆍", "wezterm": "󰆍", "ghostty": "󰆍", 
    "gnome-terminal": "󰆍", "konsole": "󰆍", "xterm": "󰆍", "st": "󰆍", "urxvt": "󰆍", 
    "term": "󰆍", "tilix": "󰆍", "lxterminal": "󰆍", "xfce4-terminal": "󰆍", "tabby": "󰆍",
    "hyper": "󰆍", "rio": "󰆍", "tilda": "󰆍", "guake": "󰆍", "yakuake": "󰆍",

    # --- Web Browsers ---
    "brave": "", "brave-browser": "", "brave-desktop": "", "google-chrome": "󰊯", "chrome": "󰊯",
    "firefox": "󰈹", "firefox-developer-edition": "󰈹", "firefox-nightly": "󰈹",
    "chromium": "󰈹", "zen": "󰈹", "zen-browser": "󰈹", "librewolf": "󰈹", "vivaldi": "󰈹", "opera": "󰈹", 
    "tor-browser": "󰈹", "epiphany": "󰈹", "qutebrowser": "󰈹", "midori": "󰈹", "falkon": "󰈹", 
    "floorp": "󰈹", "waterfox": "󰈹", "pale-moon": "󰈹", "browser": "󰈹",


    # --- Code Editors, IDEs & Development ---
    "code": "󰨞", "code-oss": "󰨞", "vscode": "󰨞", "vscodium": "󰨞", "cursor": "󰨞",
    "neovim": "󰅩", "nvim": "󰅩", "vim": "󰅩", "gvim": "󰅩", "emacs": "", 
    "sublime_text": "󰅩", "sublime-text": "󰅩", "subl": "󰅩", "zed": "󰅩",
    "clion": "󰨞", "pycharm": "󰨞", "intellij": "󰨞", "idea": "󰨞", "webstorm": "󰨞", 
    "phpstorm": "󰨞", "rider": "󰨞", "goland": "󰨞", "rubymine": "󰨞", "datagrip": "󰨞",
    "android-studio": "󰨞", "kate": "󰅩", "kwrite": "󰅩", "geany": "󰅩", "gedit": "󰅩", 
    "mousepad": "󰅩", "pluma": "󰅩", "postman": "󰛦", "insomnia": "󰛦", "dbeaver": "󰆼",
    "mysql-workbench": "󰆼", "git-kraken": "󰊢", "sourcetree": "󰊢", "editor": "󰅩",

    # --- File Managers & Archive Utilities ---
    "thunar": "󰉋", "nemo": "󰉋", "nautilus": "󰉋", "dolphin": "󰉋", "pcmanfm": "󰉋", 
    "pcmanfm-qt": "󰉋", "ranger": "󰉋", "yazi": "󰉋", "nnn": "󰉋", "lf": "󰉋", 
    "doublecmd": "󰉋", "krusader": "󰉋", "file-roller": "󰉋", "ark": "󰉋", "fm": "󰉋",

    # --- Media Players, Audio & Video ---
    "spotify": "󰓇", "vlc": "󰕼", "mpv": "󰕼", "audacious": "󰓇", "ncmpcpp": "󰓇", 
    "rhythmbox": "󰓇", "cmus": "󰓇", "clementine": "󰓇", "strawberry": "󰓇", "deadbeef": "󰓇",
    "music": "󰓇", "obs": "󰕧", "obs-studio": "󰕧", "kdenlive": "󰕧", "handbrake": "󰕧", 
    "shotcut": "󰕧", "davinci-resolve": "󰕧", "audacity": "󰓇", "ardour": "󰓇",

    # --- Communication, Chat & Social ---
    "discord": "󰙯", "vesktop": "󰙯", "webcord": "󰙯", "equibop": "󰙯", "armcord": "󰙯",
    "telegram": "", "telegram-desktop": "", "signal": "󰈎", "element": "󰈎", 
    "slack": "󰒱", "whatsapp": "󰈎", "whatsapp-for-linux": "󰈎", "teams": "󰈎", 
    "skype": "󰈎", "zoom": "󰈎", "thunderbird": "󰇮", "geary": "󰇮", "evolution": "󰇮",

    # --- Gaming, Launchers & Emulators ---
    "steam": "󰓓", "heroic": "󰓓", "lutris": "󰓓", "bottles": "󰓓", "minecraft": "󰓓", 
    "prism": "󰓓", "prism-launcher": "󰓓", "retroarch": "󰓓", "pcsx2": "󰓓", 
    "rpcs3": "󰓓", "yuzu": "󰓓", "ryujinx": "󰓓", "dolphin-emu": "󰓓",

    # --- Graphics, Design & 3D Modeling ---
    "gimp": "󰄄", "inkscape": "󰄄", "blender": "󰂫", "krita": "󰄄", "darktable": "󰄄", 
    "rawtherapee": "󰄄", "digikam": "󰄄", "feh": "󰄄", "sxiv": "󰄄", "nsxiv": "󰄄", 
    "eog": "󰄄", "gwenview": "󰄄", "loupe": "󰄄", "viewnior": "󰄄",

    # --- Office, Reading & Productivity ---
    "obsidian": "󰏫", "libreoffice": "󰏫", "libreoffice-writer": "󰏫", 
    "libreoffice-calc": "󰏫", "libreoffice-impress": "󰏫", "onlyoffice": "󰏫", 
    "wps": "󰏫", "evince": "󰈦", "zathura": "󰈦", "okular": "󰈦", "mupdf": "󰈦", 
    "xreader": "󰈦", "notion": "󰏫", "anytype": "󰏫", "logseq": "󰏫",

    # --- System Control, Virtualization & Utilities ---
    "pavucontrol": "󰕾", "wireplumber": "󰕾", "pipewire": "󰕾", "htop": "󰄨", "btop": "󰄨", 
    "gparted": "󰋊", "timeshift": "󰁯", "virt-manager": "󰢹", "virtualbox": "󰢹", 
    "vmware": "󰢹", "qemu": "󰢹", "docker": "󰡨", "bitwarden": "󰌋", "1password": "󰌋", 
    "keepassxc": "󰌋", "calculator": "󰪚", "gnome-calculator": "󰪚", "kcalc": "󰪚"
}

def resolve_icon(app_class, app_title):
    cls = (app_class or "").lower()
    ttl = (app_title or "").lower()
    
    # Tier 1: Direct key lookup
    if cls in ICON_MAP:
        return ICON_MAP[cls]
    
    # Tier 2: Substring matching against registered app keys
    for key, icon in ICON_MAP.items():
        if key in cls or key in ttl:
            return icon
            
    # Tier 3: Category Fallback Inspection
    if any(k in cls or k in ttl for k in ["term", "console", "tty", "shell", "pty"]): return "󰆍"
    if any(k in cls or k in ttl for k in ["browser", "web", "http", "site", "html"]): return "󰈹"
    if any(k in cls or k in ttl for k in ["edit", "code", "text", "dev", "ide", "script"]): return "󰅩"
    if any(k in cls or k in ttl for k in ["file", "folder", "fm", "dir", "archive", "zip"]): return "󰉋"
    if any(k in cls or k in ttl for k in ["music", "audio", "player", "sound", "volume", "song"]): return "󰓇"
    if any(k in cls or k in ttl for k in ["video", "movie", "media", "film", "stream"]): return "󰕼"
    if any(k in cls or k in ttl for k in ["chat", "messenger", "social", "mail", "email", "talk"]): return "󰈎"
    if any(k in cls or k in ttl for k in ["game", "play", "emu", "arcade"]): return "󰓓"
    if any(k in cls or k in ttl for k in ["image", "photo", "draw", "gfx", "paint", "pic"]): return "󰄄"
    if any(k in cls or k in ttl for k in ["doc", "pdf", "note", "office", "sheet", "book"]): return "󰏫"
    if any(k in cls or k in ttl for k in ["system", "setting", "calc", "pass", "vault"]): return "󰄨"

    # Generic window fallback icon
    return "󰌽"
