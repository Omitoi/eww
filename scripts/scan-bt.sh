#!/usr/bin/env bash
bluetoothctl --timeout 5 scan on >/dev/null 2>&1 &
(
    sleep 3
    eww update bt_list="$(~/.config/eww/scripts/get-bt-list.py)"
) &
