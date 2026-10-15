#!/usr/bin/env python3
import os, time, re, glob
from datetime import datetime

def check_reboot_needed():
    # 1. Standard flag files
    if os.path.exists("/var/run/reboot-required") or os.path.exists("/run/reboot-required") or os.path.exists("/tmp/reboot-required"):
        return True

    # 2. Kernel modules missing for the currently running kernel
    try:
        running_k = os.uname().release
        if not os.path.isdir(f"/usr/lib/modules/{running_k}"):
            return True
    except Exception:
        pass

    # Read system boot timestamp
    boot_time = 0
    try:
        with open("/proc/uptime") as f:
            boot_time = time.time() - float(f.read().split()[0])
    except Exception:
        return False

    # 3. Kernel images / unified kernel images updated since boot
    for pattern in ["/boot/vmlinuz-*", "/boot/EFI/**/*.efi"]:
        for vf in glob.glob(pattern, recursive=True):
            try:
                if os.path.getmtime(vf) > boot_time:
                    return True
            except Exception:
                pass

    # 4. Critical packages upgraded in pacman.log since boot
    if os.path.exists("/var/log/pacman.log"):
        CRITICAL_PKGS = {
            "linux", "linux-lts", "linux-zen", "linux-hardened",
            "systemd", "glibc", "linux-firmware", "intel-ucode", "amd-ucode",
            "nvidia", "nvidia-lts", "nvidia-dkms", "mesa"
        }
        try:
            with open("/var/log/pacman.log", "rb") as f:
                f.seek(0, os.SEEK_END)
                size = f.tell()
                f.seek(max(0, size - 32768))
                lines = f.read().decode("utf-8", errors="ignore").splitlines()

            for line in lines:
                m = re.match(r"^\[([0-9T:+-]+)\] \[ALPM\] (upgraded|installed|removed) ([^ ]+)", line)
                if m:
                    ts_str, _, pkg = m.groups()
                    if len(ts_str) >= 24 and (ts_str[-5] in "+-") and (ts_str[-3] != ":"):
                        ts_str = ts_str[:-2] + ":" + ts_str[-2:]
                    try:
                        log_ts = datetime.fromisoformat(ts_str).timestamp()
                        if log_ts >= boot_time:
                            pkg_base = pkg.split(":")[0]
                            if pkg_base in CRITICAL_PKGS or pkg_base.startswith("linux-"):
                                return True
                    except Exception:
                        pass
        except Exception:
            pass

    return False

if __name__ == "__main__":
    print("true" if check_reboot_needed() else "false")
