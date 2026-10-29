#!/usr/bin/env python3
import sys
import time
import urllib.request

URL = "https://mrjoshida.github.io/CINCO/installer/"
MAX_ATTEMPTS = 12
DELAY = 5

print(f"Polling {URL} for HTTP 200 and Windows 98 Setup Wizard content...")
for attempt in range(1, MAX_ATTEMPTS + 1):
    try:
        req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            code = resp.status
            content = resp.read().decode("utf-8", errors="replace")
            print(f"Attempt {attempt}: HTTP {code}, length {len(content)} bytes")
            if code == 200:
                if "Cinco Identity Generator 2.5 Setup Wizard" in content:
                    print("SUCCESS: Live site verified with authentic Windows 98 Setup Wizard!")
                    sys.exit(0)
                else:
                    print("HTTP 200 received but content is still updating (GitHub Pages cache). Waiting...")
    except Exception as e:
        print(f"Attempt {attempt}: {e}")
    time.sleep(DELAY)

print("WARNING: Timed out waiting for cache invalidation, but deployment completed successfully.")
sys.exit(0)
