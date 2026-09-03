#!/usr/bin/env bash
# Trigger active Wi-Fi scan via iwctl
iwctl station wlan0 scan >/dev/null 2>&1 &

(
    sleep 2
    eww update wifi_list="$(~/.config/eww/scripts/get-wifi-list.py)"
) &
