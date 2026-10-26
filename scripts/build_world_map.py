#!/usr/bin/env python3
"""Write the outline of the countries that the dashboard draws under its map tiles.

The dashboard loads its map tiles from OpenStreetMap, and a browser that blocks the tile server
would otherwise show the points on a blank grey ground. The page therefore also draws the countries
from Natural Earth's map of countries at the scale of 1:110 million, which is in the public domain.
The script keeps only the name of each country and rounds the coordinates to two decimals, so that
the file stays small.

    python scripts/build_world_map.py ne_110m_admin_0_countries.geojson    writes site/data/world.geojson

The source file is at https://github.com/nvkelso/natural-earth-vector/tree/master/geojson.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "data" / "world.geojson"


def rounded(coordinates):
    if isinstance(coordinates[0], (int, float)):
        return [round(coordinates[0], 2), round(coordinates[1], 2)]
    return [rounded(c) for c in coordinates]


def outline(data: dict) -> dict:
    features = [{"type": "Feature", "properties": {"name": f["properties"].get("ADMIN", "")},
                 "geometry": {"type": f["geometry"]["type"], "coordinates": rounded(f["geometry"]["coordinates"])}}
                for f in data["features"] if f.get("geometry")]
    return {"type": "FeatureCollection", "features": features}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", type=Path, help="Natural Earth file of countries at 1:110m, in GeoJSON")
    args = parser.parse_args()
    world = outline(json.loads(args.source.read_text()))
    OUT.write_text(json.dumps(world, separators=(",", ":")) + "\n")
    print(f"{len(world['features'])} countries written to {OUT.relative_to(ROOT)}, {OUT.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
