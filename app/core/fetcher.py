from pathlib import Path
from datetime import datetime

import requests


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def fetch_url(url: str) -> str | None:
    try:
        response = requests.get(
            url,
            timeout=(5, 20),
            headers={
                "User-Agent": "Mozilla/5.0"
            },
        )
        response.raise_for_status()
        return response.text

    except requests.RequestException as e:
        print("FETCH ERROR:", e)
        return None


def save_raw(source_id: str, raw_text: str):
    source_dir = RAW_DIR / source_id
    ensure_dir(source_dir)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = source_dir / f"{timestamp}.txt"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(raw_text)

    return file_path