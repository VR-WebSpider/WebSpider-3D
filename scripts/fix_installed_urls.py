"""
WebSpider 3D - URL Hotfix Script
Run this as Administrator to update the installed WebSpider 3D to use webspiderstudios.com.

Usage (PowerShell as Admin):
  python "E:\\WebSpider 3D\\scripts\\fix_installed_urls.py"
"""
import json
import os
import sys
import shutil
from datetime import datetime

INSTALL_DIR = r"C:\Program Files\WebSpider 3D"
CONFIG_PATH = os.path.join(INSTALL_DIR, "5.0", "config", "webspider.json")
EXE_PATH    = os.path.join(INSTALL_DIR, "webspider.exe")

OLD_FRONTEND_URL = b"https://www.webspider3d.com"
NEW_FRONTEND_URL = b"https://webspiderstudios.com\x00\x00"  # same byte count (29 = 27 + 2 nulls padding)

OLD_BACKEND_URL  = b"https://api.webspider3d.com"
NEW_BACKEND_URL  = b"https://webspiderstudios.com"  # same length? Let's check:
# OLD_BACKEND_URL  = 27 chars
# NEW_BACKEND_URL  = 29 chars  (2 chars longer)
# The binary has 5 null bytes after OLD_BACKEND_URL, so we can write 2 more chars into that space.

def backup(path: str) -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = path + f".bak_{ts}"
    shutil.copy2(path, backup_path)
    print(f"  Backed up: {backup_path}")
    return backup_path


def fix_json_config():
    print(f"\n[1] Updating JSON config: {CONFIG_PATH}")
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)

        cfg["backend_url"]  = "https://webspiderstudios.com"
        cfg["frontend_url"] = "https://webspiderstudios.com"

        backup(CONFIG_PATH)
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
        print(f"  SUCCESS: {CONFIG_PATH}")
    except PermissionError:
        print("  ERROR: Access denied. Run this script as Administrator.")
        return False
    except Exception as e:
        print(f"  ERROR: {e}")
        return False
    return True


def fix_binary():
    """
    Patch the compiled webspider.exe binary to replace webspider3d.com URLs.

    The C++ constants are stored as null-terminated strings in the .rdata section.
    We replace them in-place, which works because we use equal-or-shorter replacements
    with null padding to keep surrounding bytes intact.
    """
    print(f"\n[2] Binary-patching EXE: {EXE_PATH}")

    try:
        with open(EXE_PATH, "rb") as f:
            data = bytearray(f.read())
    except PermissionError:
        print("  ERROR: Access denied. Run this script as Administrator.")
        return False
    except FileNotFoundError:
        print(f"  ERROR: webspider.exe not found at {EXE_PATH}")
        return False

    changed = 0

    # ---- Patch 1: Frontend URL ----
    # OLD: https://www.webspider3d.com   (27 bytes + trailing nulls)
    # NEW: https://webspiderstudios.com  (29 bytes, 2 chars LONGER)
    # Safe because binary has 13+ null bytes after the old string.
    old1 = b"https://www.webspider3d.com"
    new1 = b"https://webspiderstudios.com"
    assert len(new1) > len(old1), "New URL must fit in place"
    extra1 = len(new1) - len(old1)

    idx = 0
    while True:
        pos = data.find(old1, idx)
        if pos < 0:
            break
        # Confirm there are enough null bytes after old URL to expand into
        after = data[pos + len(old1): pos + len(old1) + extra1 + 1]
        if all(b == 0 for b in after[:extra1]):
            data[pos: pos + len(new1)] = new1
            print(f"  Patched frontend URL at offset 0x{pos:08X}")
            changed += 1
        else:
            print(f"  SKIP offset 0x{pos:08X}: not enough null padding (after={after!r})")
        idx = pos + 1

    # ---- Patch 2: Backend URL ----
    # OLD: https://api.webspider3d.com   (27 bytes + trailing nulls)
    # NEW: https://webspiderstudios.com  (29 bytes, 2 chars LONGER)
    # Safe because binary has 5 null bytes after the old string.
    old2 = b"https://api.webspider3d.com"
    new2 = b"https://webspiderstudios.com"
    assert len(new2) > len(old2)
    extra2 = len(new2) - len(old2)

    idx = 0
    while True:
        pos = data.find(old2, idx)
        if pos < 0:
            break
        after = data[pos + len(old2): pos + len(old2) + extra2 + 1]
        if all(b == 0 for b in after[:extra2]):
            data[pos: pos + len(new2)] = new2
            print(f"  Patched backend URL at offset 0x{pos:08X}")
            changed += 1
        else:
            print(f"  SKIP offset 0x{pos:08X}: not enough null padding (after={after!r})")
        idx = pos + 1

    if changed == 0:
        print("  No patches applied (URLs already updated or not found).")
        return True

    # Write patched binary
    backup(EXE_PATH)
    try:
        with open(EXE_PATH, "wb") as f:
            f.write(data)
        print(f"  SUCCESS: wrote {changed} patch(es) to {EXE_PATH}")
    except PermissionError:
        print("  ERROR: Access denied writing EXE. Run as Administrator.")
        return False

    return True


if __name__ == "__main__":
    print("=" * 60)
    print("WebSpider 3D URL Hotfix - webspider3d.com -> webspiderstudios.com")
    print("=" * 60)

    if sys.platform != "win32":
        print("This script is for Windows only.")
        sys.exit(1)

    ok1 = fix_json_config()
    ok2 = fix_binary()

    print()
    if ok1 and ok2:
        print("All done! Restart WebSpider 3D for changes to take effect.")
    else:
        print("Some steps FAILED. Make sure you are running as Administrator.")
        sys.exit(1)
