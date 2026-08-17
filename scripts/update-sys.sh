#!/usr/bin/env bash
# 1. Run terminal package upgrade synchronously
kitty -e sudo pacman -Syu

# 2. Trigger immediate update count refresh in EWW when terminal closes
eww update update_count="$(~/.config/eww/scripts/updates.sh)"
