import asyncio
import aiohttp
import time
from pathlib import Path

URLS = {
    "adsb": "https://api.adsb.lol/v2/callsign/DAL517",
    "delta": "https://wifi.delta.com/api/flight-data",
    "adsb_fi": "https://opendata.adsb.fi/api/v2/callsign/DAL517",
    "adsb_ex": "https://adsbexchange.com/api/aircraft/call/DAL517/"
}

OUTDIR = Path("/usr/local/var/www/plane-to-map/timing-out")
OUTDIR.mkdir(exist_ok=True)


async def fetch(session, name, url):
    timings = {}

    start_ns = time.perf_counter_ns()
    timings["start_ns"] = start_ns

    body_file = OUTDIR / f"{start_ns}_{name}_body.bin"
    meta_file = OUTDIR / f"{start_ns}_{name}_timing.txt"



    async with session.get(url) as resp:
        timings["status"] = resp.status

        headers_ns = time.perf_counter_ns()
        timings["headers_received_ns"] = headers_ns

        total_bytes = 0
        last_byte_ns = None

        with open(body_file, "wb") as f:
            async for chunk in resp.content.iter_chunked(8192):
                if chunk:
                    f.write(chunk)
                    total_bytes += len(chunk)
                    last_byte_ns = time.perf_counter_ns()

    end_ns = last_byte_ns if last_byte_ns else time.perf_counter_ns()
    timings["last_byte_ns"] = end_ns
    timings["duration_ms"] = (end_ns - start_ns) / 1_000_000
    timings["bytes"] = total_bytes

    with open(meta_file, "w") as f:
        for k, v in timings.items():
            f.write(f"{k}: {v}\n")

    print(f"{name}: {timings['duration_ms']:.2f} ms ({total_bytes} bytes)")


async def main():
    timeout = aiohttp.ClientTimeout(total=60)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        # barrier so they start as close together as possible
        await asyncio.gather(
            fetch(session, "adsb", URLS["adsb"]),
            fetch(session, "delta", URLS["delta"]),
            fetch(session, "adsb_fi", URLS["adsb_fi"]),
            fetch(session, "adsb_ex", URLS["adsb_ex"])
        )


if __name__ == "__main__":
    asyncio.run(main())