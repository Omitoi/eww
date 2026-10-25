#!/usr/bin/env bash
# Open EWW bars and desktop splashes dynamically for all connected monitors

# Wait for eww daemon to be ready (up to 5s)
for i in {1..25}; do
    eww ping >/dev/null 2>&1 && break
    sleep 0.2
done

eww ping >/dev/null 2>&1 || exit 1

for mon_id in $(hyprctl monitors -j 2>/dev/null | jq -r '.[].id'); do
    eww --no-daemonize open "bar_${mon_id}"
    eww --no-daemonize open "verse_splash_${mon_id}"
done
