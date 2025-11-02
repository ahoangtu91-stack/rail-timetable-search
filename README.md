🚆 Rail Timetable Search

A command-line Python tool to search and display rail timetables using GTFS (General Transit Feed Specification) data.

📖 Overview

Rail Timetable Search lets you query train schedules for a given station and time range.
It loads GTFS feed data (static or from a remote URL) and outputs timetable results in text or JSON format.

🧰 Features

Search for departures and arrivals by station name

Filter by date, time range, or route

Supports local or remote GTFS data

Optional JSON output for automation or API use

⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/ahoangtu91-stack/rail-timetable-search.git
cd rail-timetable-search

2️⃣ Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\activate     # on Windows
# source venv/bin/activate  # on macOS/Linux

3️⃣ Install dependencies
pip install -r requirements.txt

🚀 Usage

Run the CLI directly:

python -m src.rail_nextday.cli --station "Berlin"

Optional arguments
Argument	Description	Example
--station	(Required) Station name to search for	--station "Berlin"
--date	Date of travel (YYYY-MM-DD)	--date 2025-11-02
--from	Start time (HH:MM)	--from 08:00
--to	End time (HH:MM)	--to 10:00
--route	Filter by route name or ID	--route RE1
--json	Output results in JSON format	--json
--gtfs-url	Load GTFS data from a remote URL	--gtfs-url "https://example.com/gtfs.zip"
Example
python -m src.rail_nextday.cli --station "Berlin Hbf" --from 08:00 --to 12:00

🧪 Running Tests

If you have test files under tests/:

pytest

🧩 Project Structure
rail-timetable-search/
├── src/
│   └── rail_nextday/
│       ├── cli.py
│       ├── gtfs_loader.py
│       ├── timetable.py
│       └── __init__.py
├── tests/
├── requirements.txt
├── README.md
└── pyproject.toml
