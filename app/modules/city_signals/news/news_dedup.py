import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[3]

SEEN_NEWS_PATH = (
    BASE_DIR / "data" / "system" / "seen_news.json"
)


def load_seen_news() -> set:
    if not SEEN_NEWS_PATH.exists():
        return set()

    try:
        data = json.loads(
            SEEN_NEWS_PATH.read_text(encoding="utf-8")
        )
        return set(data)
    except Exception:
        return set()


def save_seen_news(signal_id: str) -> None:
    seen = load_seen_news()

    seen.add(signal_id)

    SEEN_NEWS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    SEEN_NEWS_PATH.write_text(
        json.dumps(
            sorted(seen),
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def filter_new_news(signals: list) -> list:
    seen = load_seen_news()

    return [
        signal
        for signal in signals
        if signal.get("signal_id") not in seen
    ]