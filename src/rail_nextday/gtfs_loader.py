from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from zipfile import ZipFile
import time, urllib.request
import pandas as pd

# SNCF open GTFS feed (France)
SNCF_GTFS_URL = "https://eu.ftp.opendata.sncf.com/GTFS/gtfs.zip"

@dataclass(frozen=True)
class GTFSSource:
    url: str = SNCF_GTFS_URL
    cache_dir: Path = Path(".gtfs_cache")
    filename: str = "feed.zip"

    def local_path(self) -> Path:
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        return self.cache_dir / self.filename

    def fetch(self, max_age_hours: int = 24) -> Path:
        lp = self.local_path()
        if lp.exists() and (time.time() - lp.stat().st_mtime) < max_age_hours * 3600:
            return lp
        print("Downloading latest GTFS data ...")
        with urllib.request.urlopen(self.url) as r:
            data = r.read()
        lp.write_bytes(data)
        return lp

    def _read_csv(self, zf: ZipFile, name: str, **kwargs) -> pd.DataFrame:
        try:
            with zf.open(name) as fh:
                return pd.read_csv(fh, dtype=str, **kwargs)
        except KeyError:
            return pd.DataFrame()

    def load_tables(self) -> dict[str, pd.DataFrame]:
        path = self.fetch()
        with ZipFile(path) as zf:
            return {
                "calendar": self._read_csv(zf, "calendar.txt"),
                "calendar_dates": self._read_csv(zf, "calendar_dates.txt"),
                "stops": self._read_csv(zf, "stops.txt"),
                "trips": self._read_csv(zf, "trips.txt"),
                "routes": self._read_csv(zf, "routes.txt"),
                "stop_times": self._read_csv(zf, "stop_times.txt"),
            }
