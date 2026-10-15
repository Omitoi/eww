#!/usr/bin/env bash
# Open EWW bars and desktop splashes dynamically for all connected monitors

eww ping >/dev/null 2>&1 || exit 1

for mon_id in $(hyprctl monitors -j 2>/dev/null | jq -r '.[].id'); do
    eww open "bar_${mon_id}"
    eww open "verse_splash_${mon_id}"
done
