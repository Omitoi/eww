#!/usr/bin/env bash
# 1. Run terminal package upgrade synchronously
kitty -e sudo pacman -Syu --noconfirm

# 2. Trigger immediate update count and reboot status refresh in EWW when terminal closes
eww update update_count="$(checkupdates 2>/dev/null | wc -l)" needs_reboot="$(~/.config/eww/scripts/check-reboot.py)"
