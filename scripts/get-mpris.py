#!/usr/bin/env python3
import json
import select
import subprocess
import sys
import time

def emit(status="Stopped", artist="", title="", player=""):
    text = ""
    if title:
        text = f"{artist} - {title}" if artist else title
    text = text.replace("\n", " ").strip()
    data = {
        "status": status,
        "artist": artist.strip(),
        "title": title.strip(),
        "text": text,
        "player": player.strip(),
    }
    sys.stdout.write(json.dumps(data) + "\n")
    sys.stdout.flush()

def has_active_players():
    try:
        res = subprocess.run(
            ["playerctl", "-l"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=1
        )
        return bool(res.stdout.strip())
    except Exception:
        return False

def main():
    emit()
    last_status = "Stopped"

    cmd = [
        "stdbuf",
        "-oL",
        "playerctl",
        "-F",
        "metadata",
        "--format",
        "{{status}}||{{artist}}||{{title}}||{{playerName}}"
    ]

    while True:
        proc = None
        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                bufsize=1
            )

            while True:
                r, _, _ = select.select([proc.stdout], [], [], 2.0)
                if r:
                    line = proc.stdout.readline()
                    if not line:
                        break
                    parts = line.strip().split("||")
                    if len(parts) >= 4:
                        status, artist, title, player = parts[0], parts[1], parts[2], parts[3]
                        last_status = status
                        emit(status, artist, title, player)
                    elif len(parts) >= 1 and parts[0]:
                        last_status = parts[0]
                        emit(status=parts[0])
                else:
                    if not has_active_players():
                        if last_status != "Stopped":
                            last_status = "Stopped"
                            emit("Stopped")

        except Exception:
            pass
        finally:
            if proc:
                try:
                    proc.terminate()
                    proc.wait(timeout=0.5)
                except Exception:
                    pass

        if not has_active_players() and last_status != "Stopped":
            last_status = "Stopped"
            emit("Stopped")
        time.sleep(1)

if __name__ == "__main__":
    main()
