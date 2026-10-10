"""
EduLift AI - Persistent Server & Tunnel Watchdog
Automatically keeps the Flask web application and Cloudflare public tunnel running.
If the connection drops, it automatically reconnects and saves the active link to ACTIVE_LINK.txt.
"""

import os
import re
import sys
import time
import subprocess
import urllib.request

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
CLOUDFLARED_EXE = os.path.join(PROJECT_DIR, "cloudflared.exe")
LINK_FILE = os.path.join(PROJECT_DIR, "ACTIVE_LINK.txt")


def is_flask_running():
    try:
        resp = urllib.request.urlopen("http://127.0.0.1:5000/health", timeout=2)
        return resp.status == 200
    except Exception:
        return False


def start_flask_server():
    if not is_flask_running():
        print("[Watchdog] Starting local Flask application (app.py)...")
        subprocess.Popen([sys.executable, "app.py"], cwd=PROJECT_DIR)
        for _ in range(10):
            time.sleep(1)
            if is_flask_running():
                print("[Watchdog] Flask server is active on http://127.0.0.1:5000/")
                return True
        print("[Watchdog] Warning: Flask server taking longer than usual to report healthy.")
    else:
        print("[Watchdog] Flask server is already running on http://127.0.0.1:5000/")
    return True


def run_persistent_tunnel():
    if not os.path.exists(CLOUDFLARED_EXE):
        print(f"[Watchdog] Error: {CLOUDFLARED_EXE} not found.")
        return

    print("=" * 65)
    print("  EduLift AI — Persistent Watchdog Running")
    print("  Local URL: http://localhost:5000 (Never expires)")
    print("=" * 65)

    while True:
        start_flask_server()
        print("\n[Watchdog] Requesting active public HTTPS tunnel...")
        
        proc = subprocess.Popen(
            [CLOUDFLARED_EXE, "tunnel", "--url", "http://127.0.0.1:5000"],
            cwd=PROJECT_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        tunnel_url = None
        for line in proc.stdout:
            # Look for trycloudflare.com URL pattern
            match = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line)
            if match and not tunnel_url:
                tunnel_url = match.group(0)
                print("\n" + "=" * 65)
                print(f"🔥 ACTIVE PUBLIC LIVE URL:")
                print(f"👉 {tunnel_url}")
                print(f"👉 Login Portal: {tunnel_url}/login")
                print("=" * 65)
                with open(LINK_FILE, "w", encoding="utf-8") as f:
                    f.write(f"ACTIVE PUBLIC LINK:\n{tunnel_url}\n\nLOGIN PORTAL:\n{tunnel_url}/login\n\nLOCAL PERMANENT LINK:\nhttp://localhost:5000/\n")

            if "ERR" in line and ("timeout" in line or "Tunnel not found" in line):
                print(f"[Watchdog] Tunnel network notice: {line.strip()}")
                break

        print("[Watchdog] Tunnel disconnected or reset. Auto-reconnecting in 3 seconds...")
        time.sleep(3)


if __name__ == "__main__":
    run_persistent_tunnel()
