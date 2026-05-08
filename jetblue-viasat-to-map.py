#!/usr/bin/env python3
import re
import subprocess
import urllib.request

URL = "https://www.flyfi.com/travel/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
}

req = urllib.request.Request(URL, headers=HEADERS)
with urllib.request.urlopen(req, timeout=30) as resp:
    html = resp.read().decode("utf-8", errors="replace")

lat = float(re.search(r"travelMapData\.lat2\s*=\s*(-?\d+\.?\d*)", html).group(1))
lon = float(re.search(r"travelMapData\.lon2\s*=\s*(-?\d+\.?\d*)", html).group(1))
geo = f"geo:{lat},{lon}?z=9"
print(geo)
subprocess.run(["open", geo], check=True)
