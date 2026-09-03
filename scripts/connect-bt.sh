#!/usr/bin/env bash
if [ -z "$1" ]; then
    exit 1
fi
MAC="$1"

# Check if currently connected
if bluetoothctl info "$MAC" | grep -q "Connected: yes"; then
    bluetoothctl disconnect "$MAC"
else
    # Correct order: 1. Pair -> 2. Trust -> 3. Connect
    bluetoothctl pair "$MAC" >/dev/null 2>&1
    bluetoothctl trust "$MAC" >/dev/null 2>&1
    bluetoothctl connect "$MAC"
fi

(
    sleep 1
    eww update bt_info="$(~/.config/eww/scripts/get-bt.py)"
    eww update bt_list="$(~/.config/eww/scripts/get-bt-list.py)"
    eww update audio_sinks="$(~/.config/eww/scripts/get-audio-sinks.py)"
) &
