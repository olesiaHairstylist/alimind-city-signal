import requests
from datetime import datetime
from pathlib import Path


URL = "https://www.yenialanya.com/rss"

BASE_DIR = Path(__file__).resolve().parents[3]

RAW_DIR = (
    BASE_DIR / "data" / "raw" / "news" / "yeni_alanya"
)


def fetch_yeni_alanya() -> str | None:
    try:
        response = requests.get(
            URL,
            timeout=25,
            headers={
                "User-Agent": "Mozilla/5.0",
            },
        )

        if response.status_code != 200:
            print("YENI ALANYA FETCH ERROR:", response.status_code)
            return None

        return response.text

    except Exception as e:
        print("YENI ALANYA FETCH CRASH:", e)
        return None


def save_raw_yeni_alanya(raw_text: str) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    filename = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S.xml")

    path = RAW_DIR / filename

    path.write_text(raw_text, encoding="utf-8")

    return path


if __name__ == "__main__":
    print("FETCH SOURCE: yeni_alanya")

    raw = fetch_yeni_alanya()

    if raw is None:
        print("NO RAW DATA")
    else:
        path = save_raw_yeni_alanya(raw)
        print("RAW SAVED:", path)
        print("RAW LENGTH:", len(raw))