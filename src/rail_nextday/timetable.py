from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
import pandas as pd
from .gtfs_loader import GTFSSource

EU_TZ = ZoneInfo("Europe/Paris")

@dataclass(frozen=True)
class Departure:
    time: str
    trip_id: str
    route_id: str
    route_name: str
    headsign: str
    stop_name: str

def _yyyymmdd(d: date) -> str:
    return d.strftime("%Y%m%d")

from datetime import date
import pandas as pd

def service_ids_for(d: date, tables: dict[str, pd.DataFrame]) -> set[str]:
    """
    Return service_ids active on date d.
    Works when:
      - calendar.txt exists, and/or
      - calendar_dates.txt exists (exception-only feeds)
    """
    ymd = d.strftime("%Y%m%d")
    svc: set[str] = set()

    # 1) calendar.txt (if present)
    cal = tables.get("calendar", pd.DataFrame())
    if not cal.empty:
        weekday = d.strftime("%A").lower()
        base = cal[
            (cal[weekday] == "1")
            & (cal["start_date"] <= ymd)
            & (cal["end_date"] >= ymd)
        ]["service_id"].astype(str).tolist()
        svc |= set(base)

    # 2) calendar_dates.txt (adds/removes) — also supports exception-only feeds
    cd = tables.get("calendar_dates", pd.DataFrame())
    if not cd.empty:
        adds = cd[(cd["date"] == ymd) & (cd["exception_type"] == "1")]["service_id"].astype(str)
        rems = cd[(cd["date"] == ymd) & (cd["exception_type"] == "2")]["service_id"].astype(str)
        svc |= set(adds)
        svc -= set(rems)

    return svc

    cal = tables.get("calendar", pd.DataFrame()).copy()
    if cal.empty:
        return set()
    weekday = d.strftime("%A").lower()
    active = cal[
        (cal[weekday] == "1")
        & (cal["start_date"] <= _yyyymmdd(d))
        & (cal["end_date"] >= _yyyymmdd(d))
    ]["service_id"].astype(str).tolist()

    svc = set(active)
    cd = tables.get("calendar_dates", pd.DataFrame())
    if not cd.empty:
        adds = cd[(cd["date"] == _yyyymmdd(d)) & (cd["exception_type"] == "1")]["service_id"]
        rems = cd[(cd["date"] == _yyyymmdd(d)) & (cd["exception_type"] == "2")]["service_id"]
        svc |= set(adds.astype(str))
        svc -= set(rems.astype(str))
    return svc

def build_timetable_for_station(
    station_query: str,
    target_date: date | None,
    source: GTFSSource = GTFSSource(),
    time_window: tuple[str, str] | None = None,
    route_filter: str | None = None,
) -> list[Departure]:
    t = source.load_tables()
    d = target_date or (datetime.now(EU_TZ).date() + timedelta(days=1))
    svc = service_ids_for(d, t)

    trips = t["trips"]
    routes = t["routes"]
    stops = t["stops"]
    stop_times = t["stop_times"]

    station_candidates = stops[stops["stop_name"].str.contains(station_query, case=False, na=False)]
    if station_candidates.empty:
        return []

    stop_ids = set(station_candidates["stop_id"].astype(str))
    st = stop_times[stop_times["stop_id"].isin(stop_ids)].copy()

    if time_window:
        start, end = time_window
        st = st[(st["departure_time"] >= start) & (st["departure_time"] <= end)]

    day_trips = trips[trips["service_id"].isin(svc)].copy()
    merged = (
        st.merge(day_trips, on="trip_id", how="inner")
          .merge(routes, on="route_id", how="left", suffixes=("", "_route"))
          .merge(stops[["stop_id","stop_name"]], on="stop_id", how="left")
    )

    if route_filter:
        mask = merged["route_short_name"].fillna("") + " " + merged["route_long_name"].fillna("")
        merged = merged[mask.str.contains(route_filter, case=False, na=False)]

    merged = merged.sort_values(["departure_time", "route_id", "trip_id"])

    results: list[Departure] = []
    for _, r in merged.iterrows():
        results.append(Departure(
            time=str(r["departure_time"]),
            trip_id=str(r["trip_id"]),
            route_id=str(r["route_id"]),
            route_name=str(r.get("route_long_name") or r.get("route_short_name") or ""),
            headsign=str(r.get("trip_headsign") or ""),
            stop_name=str(r.get("stop_name") or ""),
        ))
    return results
