#!/usr/bin/env python3
import subprocess
import time
import requests

# ───────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ───────────────────────────────────────────────────────────────────────────────
WG_CONTAINER         = "wireguard"
WG_INTERFACE         = "wg0"
CHECK_INTERVAL       = 5      # seconds between checks
DISCONNECT_THRESHOLD = 30     # seconds with no handshake → disconnected
ALERT_URL            = "http://<YOUR_BACKEND_HOST>:<PORT>/api/vpn-disconnect"
# ───────────────────────────────────────────────────────────────────────────────

_last_reported = {}  # pubkey -> last_handshake

def get_peers():
    cmd = [
        "docker", "exec", WG_CONTAINER,
        "wg", "show", WG_INTERFACE, "dump"
    ]
    try:
        out = subprocess.check_output(cmd, text=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] failed to exec wg: {e}")
        return []

    peers = []
    for line in out.strip().splitlines()[1:]:
        cols = line.split("\t")
        if len(cols) >= 5:
            pubkey = cols[0]
            last_hs = int(cols[4])
            peers.append((pubkey, last_hs))
    return peers

def alert_disconnect(pubkey, last_hs):
    payload = {
        "pubkey": pubkey,
        "last_handshake": last_hs,
        "timestamp": int(time.time())
    }
    try:
        r = requests.post(ALERT_URL, json=payload, timeout=5)
        print(f"[ALERT] {pubkey} disconnected → {r.status_code}")
    except Exception as e:
        print(f"[ERROR] alert failed for {pubkey}: {e}")

def monitor():
    print(f"[*] Starting VPN disconnect monitor (via `docker exec`)…")
    while True:
        now = int(time.time())
        for pubkey, last_hs in get_peers():
            age = now - last_hs
            # If older than threshold and not yet reported
            if age > DISCONNECT_THRESHOLD and _last_reported.get(pubkey) != last_hs:
                print(f"alerting for {pubkey} because last handshake is {age} seconds ago")
                alert_disconnect(pubkey, last_hs)
                _last_reported[pubkey] = last_hs
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor()
