#!/usr/bin/env bash
if [ -z "$1" ]; then
    exit 1
fi
MAC="$1"

# Check if currently connected
if bluetoothctl info "$MAC" | grep -q "Connected: yes"; then
    bluetoothctl disconnect "$MAC"
else
    bluetoothctl connect "$MAC"
fi

(
    sleep 1
    eww update bt_info="$(~/.config/eww/scripts/get-bt.py)"
    eww update bt_list="$(~/.config/eww/scripts/get-bt-list.py)"
) &
