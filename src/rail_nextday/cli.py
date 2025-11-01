from __future__ import annotations
import argparse, json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from .gtfs_loader import GTFSSource
from .timetable import build_timetable_for_station

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Next-day train timetable from open GTFS")
    p.add_argument("--station", required=True, help="Station name (e.g., 'Paris Gare de Lyon')")
    p.add_argument("--date", help="YYYY-MM-DD (defaults to tomorrow in Europe/Paris)")
    p.add_argument("--from", dest="from_time", help="HH:MM (optional filter)")
    p.add_argument("--to", dest="to_time", help="HH:MM (optional filter)")
    p.add_argument("--route", help="Route filter text (optional)")
    p.add_argument("--json", action="store_true", help="Output JSON")
    p.add_argument("--gtfs-url", help="Override GTFS URL (defaults to SNCF)")
    args = p.parse_args(argv)

    d = None
    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d").date()
    tz = ZoneInfo("Europe/Paris")
    if d is None:
        d = (datetime.now(tz) + timedelta(days=1)).date()

    src = GTFSSource(url=args.gtfs_url) if args.gtfs_url else GTFSSource()
    window = (args.from_time, args.to_time) if args.from_time and args.to_time else None

    deps = build_timetable_for_station(
        station_query=args.station,
        target_date=d,
        source=src,
        time_window=window,
        route_filter=args.route,
    )

    if args.json:
        print(json.dumps([dep.__dict__ for dep in deps], ensure_ascii=False, indent=2))
    else:
        print(f"Timetable for {args.station} on {d.isoformat()} (next-day):")
    if not deps:
        print("  No departures found.")
    for dep in deps:
        route = dep.route_name or dep.route_id
        head = dep.headsign or ""
        print(f"  {dep.time}  {route[:40]:<40}  {head}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
