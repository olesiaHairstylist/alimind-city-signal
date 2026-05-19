from pathlib import Path

from app.modules.city_signals.earthquake.usgs_parser import (
    parse_usgs_geojson,
)


BASE_DIR = Path(__file__).resolve().parents[3]
RAW_USGS_DIR = BASE_DIR / "data" / "raw" / "usgs"


def get_latest_raw_file():
    files = sorted(
        RAW_USGS_DIR.glob("*.txt"),
        reverse=True,
    )

    if not files:
        raise RuntimeError("No USGS raw files found")

    return files[0]


def main():
    raw_file = get_latest_raw_file()

    print("RAW FILE:", raw_file)

    raw_text = raw_file.read_text(
        encoding="utf-8"
    )

    events = parse_usgs_geojson(raw_text)

    print("EVENTS COUNT:", len(events))

    for event in events[:5]:
        print(event)

    print("USGS_PARSER_V1 OK")


if __name__ == "__main__":
    main()