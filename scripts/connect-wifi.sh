#!/usr/bin/env bash
if [ -z "$1" ]; then
    exit 1
fi
SSID="$1"

# 1. Optimistic UI update immediately (assume connection attempt in progress)
eww update net_info="{\"connected\": true, \"ssid\": \"Connecting...\", \"icon\": \"󰤨\", \"label\": \"$SSID\"}"

# 2. Try connecting directly first (for saved/known networks)
if ! iwctl station wlan0 connect "$SSID" 2>/dev/null; then
    # Start an asynchronous radio scan to verify network presence in background while user types
    iwctl station wlan0 scan >/dev/null 2>&1 &

    PASSWORD=""
    if command -v rofi >/dev/null 2>&1; then
        PASSWORD=$(rofi -dmenu -password -p "Enter Wi-Fi Password for $SSID:" -theme ~/.config/rofi/wifi-prompt.rasi)
    elif command -v wofi >/dev/null 2>&1; then
        PASSWORD=$(wofi --dmenu --password --prompt "Enter Wi-Fi Password for $SSID:")
    elif command -v zenity >/dev/null 2>&1; then
        PASSWORD=$(zenity --password --title="Wi-Fi Authentication" --text="Enter password for $SSID:")
    fi

    if [ -n "$PASSWORD" ]; then
        # Verify network availability from updated scan results before attempting connect
        if iwctl station wlan0 get-networks | grep -Fq "$SSID"; then
            iwctl station wlan0 connect "$SSID" --passphrase "$PASSWORD"
        fi
    fi
fi

# 3. Final state synchronization in background
(
    sleep 1
    eww update net_info="$(~/.config/eww/scripts/get-net.py)"
    eww update wifi_list="$(~/.config/eww/scripts/get-wifi-list.py)"
) &

