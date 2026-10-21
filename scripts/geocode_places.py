#!/usr/bin/env python3
"""Find a map point for every city in the site and cloud region layers, from OpenStreetMap.

The dashboard places each site at the centre of its city, not at the building, because most
sources name the city only. The script asks the Nominatim service of OpenStreetMap for each city
and country once, at most one request a second as the service's usage policy asks, and records the
point with the OpenStreetMap object that it comes from in config/places.csv. A place already in the
file is not asked again, so a person can correct a point by editing its row.

    python scripts/geocode_places.py
"""

from __future__ import annotations

import csv
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLACES_CSV = ROOT / "config" / "places.csv"
LAYERS = [ROOT / "data" / "sites.csv", ROOT / "data" / "cloud_regions.csv"]
NOMINATIM = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "overseas_data_centres_china research (github.com/newlivehung123123/overseas_data_centres_china)"
FIELDS = ["city", "country", "lat", "lon", "osm_type", "osm_id", "display_name", "source_url"]


def wanted() -> list[tuple[str, str]]:
    places = set()
    for path in LAYERS:
        with path.open(newline="") as f:
            for row in csv.DictReader(f):
                places.add((row["city"], row["country"]))
    return sorted(places)


def ask(city: str, country: str) -> dict:
    query = ", ".join(part for part in (city, country) if part)
    params = {"q": query, "format": "json", "limit": 1}
    url = f"{NOMINATIM}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        found = json.loads(response.read())
    row = {"city": city, "country": country, "source_url": url}
    if found:
        hit = found[0]
        row.update(lat=hit["lat"], lon=hit["lon"], osm_type=hit["osm_type"], osm_id=hit["osm_id"],
                   display_name=hit["display_name"])
    return row


def main() -> None:
    known = {}
    if PLACES_CSV.exists():
        with PLACES_CSV.open(newline="") as f:
            known = {(r["city"], r["country"]): r for r in csv.DictReader(f)}
    for city, country in wanted():
        if (city, country) in known:
            continue
        known[(city, country)] = ask(city, country)
        print(f"  {city}, {country}: {known[(city, country)].get('display_name', 'not found')}")
        time.sleep(1.1)
    with PLACES_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(sorted(known.values(), key=lambda r: (r["country"], r["city"])))
    missing = [k for k, r in known.items() if not r.get("lat")]
    print(f"{len(known)} places in {PLACES_CSV.relative_to(ROOT)}, {len(missing)} without a point: {missing}")


if __name__ == "__main__":
    main()
