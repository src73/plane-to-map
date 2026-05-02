#!/usr/bin/env python3
import json
import subprocess
import urllib.request

URL = "https://www.unitedwifi.com/flightaware/v1//graphql"
PAYLOAD = {
    "operationName": "GetFlightTracks",
    "query": 'query GetFlightTracks {\n  flight0: flightById(id: \n"") {\n    id\n    trackList {\n      latitude\n      longitude\n      clock\n      gs\n      heading\n      altitude\n      type\n      __typename\n    }\n    __typename\n  }\n}',
    "variables": {},
}
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    "Accept": "application/graphql-response+json, application/graphql+json, application/json, text/event-stream, multipart/mixed",
    "Content-Type": "application/json",
    "Origin": "https://www.unitedwifi.com",
    "Referer": "https://www.unitedwifi.com/content/home/index.html",
}

req = urllib.request.Request(
    URL, data=json.dumps(PAYLOAD).encode(), headers=HEADERS, method="POST"
)
with urllib.request.urlopen(req, timeout=30) as resp:
    data = json.load(resp)

tracks = data["data"]["flight0"]["trackList"]
latest = max(tracks, key=lambda t: t["clock"])
geo = f"geo:{latest['latitude']},{latest['longitude']}?z=9"
print(geo)
subprocess.run(["open", geo], check=True)
