#!/usr/bin/env bash
# Disconnect Wi-Fi via iwctl
iwctl station wlan0 disconnect >/dev/null 2>&1

(
    sleep 0.5
    eww update net_info="$(~/.config/eww/scripts/get-net.py)"
    eww update wifi_list="$(~/.config/eww/scripts/get-wifi-list.py)"
) &
