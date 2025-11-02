🚆 Rail Timetable Search

A command-line Python tool to search and display rail timetables using GTFS (General Transit Feed Specification) data.

📖 Overview

Rail Timetable Search lets you query train schedules for a given station and time range.
It loads GTFS feed data (static or from a remote URL) and outputs timetable results in text or JSON format.
Example of where to find GTFS feed 
SNCF - https://transport.data.gouv.fr/resources/67595?locale=en
SBB - https://opentransportdata.swiss/en/cookbook/timetable-cookbook/gtfs/

🧰 Features

Search for departures and arrivals by station name

Filter by date, time range, or route

⚙️ Installation & Setup

1️⃣ Clone the repository

git clone https://github.com/ahoangtu91-stack/rail-timetable-search.git

cd rail-timetable-search

2️⃣ Create and activate a virtual environment

python -m venv venv

.\venv\Scripts\activate     # on Windows

3️⃣ Install dependencies 

pip install -r requirements.txt

🚀 Usage

Run the CLI directly:

python -m src.rail_nextday.cli --station "Berlin Hbf" --from 08:00 --to 12:00

